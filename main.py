#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主程序：Tracker 聚合与可用性校验

实现要点（对应需求 1–9）：
1) 批量读取 sources.list（忽略 # 注释与空行；支持一行多地址）
2) 并行抓取 HTTP/HTTPS 上游（超时 + 自动重试）
3) 正则切分协议：udp:// http:// https:// wss:// ltseed:// bcudp:// bchttp:// bchttps://
4) 使用 set 去重 + 过滤空白，避免生成空文件
5) 多线程并行探测（默认 32）
   - UDP：以 TCP 80 端口连通性作为近似可达性
   - HTTP/HTTPS：HEAD 请求（200–499 视为可达）
   - WSS：发起 WebSocket 握手（期望 101 切换协议）
   - ltseed/bcudp/bchttp(s)：语法校验 + 指定端口 TCP 可达（BitComet 自验证思想）
6) 每种地址可配置重试次数
7) 按协议头分组→组内字典序输出
8) 双文件结果：
   - TrackerServer/tracker.txt     可用且非空
   - TrackerServer/bad_tracker.txt 失效或空白
9) 自动创建输出目录
"""

import os
import re
import ssl
import socket
import base64
import random
from urllib.parse import urlsplit, urlunsplit
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, Tuple

import requests


# -------------------------------
# 可配置常量
# -------------------------------

SOURCES_FILE = "sources.list"

OUTPUT_DIR = "TrackerServer"
GOOD_OUTPUT = os.path.join(OUTPUT_DIR, "tracker.txt")
BAD_OUTPUT = os.path.join(OUTPUT_DIR, "bad_tracker.txt")

# 抓取上游的全局配置
FETCH_TIMEOUT = 10
FETCH_MAX_WORKERS = 16
FETCH_RETRIES = 3

# 探测配置
PROBE_TIMEOUT = 5
PROBE_MAX_WORKERS = 32  # 需求默认 32

# 协议与重试
SCHEME_RETRIES: Dict[str, int] = {
    "http": 3,
    "https": 3,
    "udp": 2,
    "wss": 2,
    "ltseed": 1,
    "bcudp": 1,
    "bchttp": 2,
    "bchttps": 2,
}

# 输出分组顺序
SCHEME_ORDER = ["http", "https", "udp", "wss", "ltseed", "bcudp", "bchttp", "bchttps"]

# 支持的协议（用于解析与过滤）
SUPPORTED_SCHEMES = tuple(["http", "https", "udp", "wss", "ltseed", "bcudp", "bchttp", "bchttps"])

# 切分一行中多个 URL 的正则（正向前瞻保留分隔符）
SPLIT_PROTOCOL_RE = re.compile(
    r"(?=(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttps?://))",
    re.IGNORECASE,
)


# -------------------------------
# 工具函数
# -------------------------------

def ensure_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def strip_comment(line: str) -> str:
    # 去掉 # 及其后的内容
    pos = line.find("#")
    if pos != -1:
        return line[:pos].strip()
    return line.strip()


def split_line_urls(line: str) -> List[str]:
    """按协议切分一行可能包含的多个 URL"""
    line = strip_comment(line)
    if not line:
        return []
    parts = [p.strip() for p in SPLIT_PROTOCOL_RE.split(line) if p.strip()]
    # re.split + 前瞻会保留前缀空白片段，过滤非协议开头的噪音
    urls = [p for p in parts if re.match(r"^(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttps?://)", p, re.I)]
    return urls


def read_sources(path: str) -> List[str]:
    urls: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            u = split_line_urls(raw)
            if u:
                urls.extend(u)
    return urls


def is_http_like(scheme: str) -> bool:
    return scheme in ("http", "https")


def default_port_for_scheme(scheme: str) -> Optional[int]:
    if scheme in ("http", "bchttp"):
        return 80
    if scheme in ("https", "bchttps", "wss"):
        return 443
    # udp/ltseed/bcudp 通常需要显式端口；返回 None 表示必须提供
    return None


def host_port_from_url(url: str) -> Tuple[Optional[str], Optional[int], str]:
    """从 URL 提取 host, port, path_query_fragment"""
    try:
        u = urlsplit(url)
    except Exception:
        return None, None, "/"
    host = u.hostname
    port = u.port
    rest = urlunsplit(("", "", u.path or "/", u.query or "", u.fragment or ""))
    return host, port, rest


def tcp_connectable(host: str, port: int, timeout: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def rand_websocket_key() -> str:
    raw = bytes(random.getrandbits(8) for _ in range(16))
    return base64.b64encode(raw).decode("ascii")


# -------------------------------
# 抓取上游（HTTP/HTTPS）
# -------------------------------

def fetch_upstream_once(url: str, timeout: int) -> Tuple[bool, List[str], str]:
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        lines: List[str] = []
        for raw in resp.text.splitlines():
            pieces = split_line_urls(raw)
            if pieces:
                lines.extend(pieces)
        return True, lines, ""
    except requests.Timeout:
        return False, [], f"超时 {timeout}秒"
    except requests.HTTPError as e:
        code = getattr(e.response, "status_code", "未知")
        return False, [], f"HTTP错误: {code}"
    except requests.ConnectionError:
        return False, [], "连接错误 (DNS或网络问题)"
    except Exception as e:
        return False, [], f"意外错误: {str(e)}"


def _fetch_with_retries(url: str, retries: int, timeout: int) -> Tuple[bool, List[str], str]:
    last_err = ""
    for i in range(max(1, retries)):
        ok, lines, err = fetch_upstream_once(url, timeout)
        if ok:
            return True, lines, ""
        last_err = f"{err} (尝试 {i+1}/{retries})"
    return False, [], last_err or "未知错误"


def fetch_upstreams_concurrently(urls: List[str]) -> Tuple[List[str], List[str]]:
    """返回 (收集到的 tracker 候选, 失败的上游列表[含原因])"""
    candidates: List[str] = []
    failed: List[str] = []

    if not urls:
        return candidates, failed

    max_workers = min(FETCH_MAX_WORKERS, max(1, len(urls)))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        future_map = {}
        for u in urls:
            future = ex.submit(_fetch_with_retries, u, FETCH_RETRIES, FETCH_TIMEOUT)
            future_map[future] = u

        for fut in as_completed(future_map):
            src = future_map[fut]
            ok, lines, err = fut.result()
            if ok:
                candidates.extend(lines)
            else:
                msg = f"{src} | {err}"
                print(f"⚠ 警告: 无法拉取 {src}: {err}")
                failed.append(msg)

    return candidates, failed


# -------------------------------
# 协议探测
# -------------------------------

def probe_http_like(url: str, retries: int, timeout: int) -> bool:
    for _ in range(max(1, retries)):
        try:
            r = requests.head(url, allow_redirects=True, timeout=timeout)
            # 200–499 视为可达
            if 200 <= r.status_code <= 499:
                return True
        except Exception:
            pass
    return False


def probe_udp_like(url: str, retries: int, timeout: int) -> bool:
    # 以 TCP 80 可连作为近似可达性
    host, _port, _ = host_port_from_url(url)
    if not host:
        return False
    target_port = 80
    for _ in range(max(1, retries)):
        if tcp_connectable(host, target_port, timeout):
            return True
    return False


def probe_ws_wss(url: str, retries: int, timeout: int) -> bool:
    # 原生 WebSocket 握手，要求返回 101
    u = urlsplit(url)
    if not u.hostname:
        return False
    host = u.hostname
    port = u.port or default_port_for_scheme(u.scheme) or 443
    path = u.path or "/"
    if u.query:
        path += "?" + u.query

    # 只实现 wss（加密）
    for _ in range(max(1, retries)):
        try:
            # TCP 连接
            with socket.create_connection((host, port), timeout=timeout) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    key = rand_websocket_key()
                    host_header = f"{host}:{port}" if port not in (80, 443) else host
                    req = (
                        f"GET {path} HTTP/1.1\r\n"
                        f"Host: {host_header}\r\n"
                        f"Upgrade: websocket\r\n"
                        f"Connection: Upgrade\r\n"
                        f"Sec-WebSocket-Key: {key}\r\n"
                        f"Sec-WebSocket-Version: 13\r\n"
                        f"Origin: https://{host}\r\n"
                        f"\r\n"
                    ).encode("ascii")
                    ssock.sendall(req)
                    ssock.settimeout(timeout)
                    # 读取响应首行与头
                    data = b""
                    while b"\r\n\r\n" not in data and len(data) < 8192:
                        chunk = ssock.recv(1024)
                        if not chunk:
                            break
                        data += chunk
                    header = data.decode("iso-8859-1", errors="ignore")
                    status_line = header.split("\r\n", 1)[0]
                    if "101" in status_line:
                        return True
        except Exception:
            continue
    return False


def probe_port_reachable(url: str, retries: int, timeout: int, require_port: bool) -> bool:
    host, port, _ = host_port_from_url(url)
    if not host:
        return False
    if port is None:
        if require_port:
            return False
        # 可根据协议推断默认端口
        scheme = urlsplit(url).scheme
        port = default_port_for_scheme(scheme)
        if port is None:
            return False
    for _ in range(max(1, retries)):
        if tcp_connectable(host, int(port), timeout):
            return True
    return False


def probe_one(url: str) -> Tuple[str, bool]:
    """返回 (url, 是否可用)"""
    scheme = urlsplit(url).scheme.lower()
    retries = SCHEME_RETRIES.get(scheme, 1)

    if scheme in ("http", "https"):
        ok = probe_http_like(url, retries, PROBE_TIMEOUT)
    elif scheme == "udp":
        ok = probe_udp_like(url, retries, PROBE_TIMEOUT)
    elif scheme == "wss":
        ok = probe_ws_wss(url, retries, PROBE_TIMEOUT)
    elif scheme in ("ltseed", "bcudp"):
        # 语法 + 端口可达（要求有端口）
        ok = probe_port_reachable(url, retries, PROBE_TIMEOUT, require_port=True)
    elif scheme in ("bchttp", "bchttps"):
        # 语法 + 端口可达（无端口则按 http/https 默认）
        ok = probe_port_reachable(url, retries, PROBE_TIMEOUT, require_port=False)
    else:
        ok = False

    return url, ok


# -------------------------------
# 主流程
# -------------------------------

def main() -> None:
    # 1) 读取 sources.list
    try:
        with open(SOURCES_FILE, encoding="utf-8"):
            pass
        print(f"ℹ 信息: 从 {os.path.abspath(SOURCES_FILE)} 读取 {SOURCES_FILE}")
    except FileNotFoundError:
        print(f"❌ 错误: {SOURCES_FILE} 文件未找到")
        raise
    except Exception as e:
        print(f"❌ 错误: 读取 {SOURCES_FILE} 失败: {str(e)}")
        raise

    source_items = read_sources(SOURCES_FILE)
    # 保留并增强提示
    print(f"✅ 读取源完成：共 {len(source_items)} 条地址")

    # 2) 将 http/https 作为上游列表地址并行抓取；其他协议视为直接候选
    upstreams = [u for u in source_items if is_http_like(urlsplit(u).scheme.lower())]
    direct_candidates = [u for u in source_items if not is_http_like(urlsplit(u).scheme.lower())]
    print(f"✅ 分类完成：上游 {len(upstreams)} 条，直接候选 {len(direct_candidates)} 条")

    fetched_candidates: List[str] = []
    failed_upstreams: List[str] = []
    if upstreams:
        fetched_candidates, failed_upstreams = fetch_upstreams_concurrently(upstreams)

    # 3) 汇总候选（含直接候选）→ 去重前计数
    all_urls: List[str] = []
    all_urls.extend(fetched_candidates)
    all_urls.extend(direct_candidates)
    print(f"✅ 成功拉取 {len(all_urls)} 条 URL 🎉")

    # 4) 去重与过滤 + 唯一计数
    unique_urls = sorted({u for u in all_urls if u.strip() and urlsplit(u).scheme.lower() in SUPPORTED_SCHEMES})
    print(f"ℹ 信息: 收集到 {len(unique_urls)} 条唯一 URL")

    # 5) 当无任何候选且有上游失败时提示（保留原始文案，不中断后续流程）
    if not unique_urls and failed_upstreams:
        print("❌ 错误: 所有源均无法访问，无有效 Tracker")

    # 6) 探测有效性
    ok_set: Set[str] = set()
    bad_set: Set[str] = set()
    if unique_urls:
        with ThreadPoolExecutor(max_workers=PROBE_MAX_WORKERS) as ex:
            futures = {ex.submit(probe_one, u): u for u in unique_urls}
            for fut in as_completed(futures):
                url, ok = fut.result()
                if ok:
                    ok_set.add(url)
                else:
                    bad_set.add(url)
    print(f"✅ 探测完成：可用 {len(ok_set)} 条，失效 {len(bad_set)} 条")

    # 7) 分组 + 组内排序
    grouped_ok: Dict[str, List[str]] = {k: [] for k in SCHEME_ORDER}
    for u in ok_set:
        s = urlsplit(u).scheme.lower()
        if s in grouped_ok:
            grouped_ok[s].append(u)
    for k in grouped_ok:
        grouped_ok[k].sort()

    # 8) 写文件（自动创建输出目录；杜绝空白 tracker.txt）
    try:
        ensure_output_dir()
        print(f"ℹ 信息: 输出目录创建于 {os.path.abspath(OUTPUT_DIR)}")
    except Exception as e:
        print(f"❌ 错误: 创建输出目录 {OUTPUT_DIR} 失败: {str(e)}")
        raise

    total_good = sum(len(v) for v in grouped_ok.values())
    if total_good > 0:
        with open(GOOD_OUTPUT, "w", encoding="utf-8") as f:
            for scheme in SCHEME_ORDER:
                if grouped_ok[scheme]:
                    for u in grouped_ok[scheme]:
                        f.write(u + "\n")
        print(f"✅ 成功写入 {total_good} 条 URL 到 {os.path.abspath(GOOD_OUTPUT)} 🎉")

    # 9) bad_tracker 输出：包含失效条目与抓取失败源
    bad_lines: List[str] = []
    if bad_set:
        bad_lines.extend(sorted(bad_set))
    if failed_upstreams:
        bad_lines.append("# 上游抓取失败：")
        bad_lines.extend(sorted(set(failed_upstreams)))
    if total_good == 0:
        bad_lines.append("[空白] 可用 Tracker 为空")

    if bad_lines:
        with open(BAD_OUTPUT, "w", encoding="utf-8") as f:
            f.write("\n".join(bad_lines) + "\n")
        # 保留原版提示
        if failed_upstreams:
            print(f"⚠ 警告: {len(failed_upstreams)} 个源无法访问，已写入 {os.path.abspath(BAD_OUTPUT)}")
    else:
        # 原版无失败源时的提示
        print("ℹ 信息: 无失败源，未生成 bad_tracker.txt")


if __name__ == "__main__":
    main()
