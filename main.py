#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracker 聚合脚本（最终可选死链验证）
"""

import os
import re
from urllib.parse import urlsplit
from typing import List, Tuple
import requests

# -------------------------------
# 配置区
# -------------------------------
SOURCES = 'sources.list'
OUTPUT = 'TrackerServer/tracker.txt'
BAD_OUTPUT = 'TrackerServer/bad_tracker.txt'
TIMEOUT = 10
MAX_RETRIES = 3

# 支持协议与输出顺序
SUPPORTED_SCHEMES = (
    "http", "https", "udp", "wss",
    "ltseed", "bcudp", "bchttp", "bchttps",
    "dht", "ptp", "ftp", "ws", "btsp", "btih"
)
SCHEME_ORDER = [
    "http", "https", "udp", "ws", "wss",
    "ltseed", "bcudp", "bchttp", "bchttps",
    "dht", "ptp", "ftp", "btsp", "btih"
]

# 死链检测开关
CHECK_URL_ALIVE = False  # True = 验证 URL 可用性，False = 只抓取不测试

# 正则切分协议
SPLIT_PROTOCOL_RE = re.compile(
    r'(?=(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttp://|bchttps://|dht://|ptp://|ftp://|ws://|btsp://|btih://))',
    re.IGNORECASE
)

# 过滤 JS / 拼接垃圾
ILLEGAL_RE = re.compile(
    r"(location\.protocol|nextChapterData|document\.|window\.|eval\(|\+.*[\'\"]|[\'\"]\+|return url|var |function\()",
    re.I
)

# -------------------------------
# 工具函数
# -------------------------------
def split_line_urls(line: str) -> List[str]:
    """按协议切分一行文本里的多个 URL，忽略 # 注释与 JS 拼接乱码。"""
    line = line.split('#', 1)[0].strip()
    if not line or ILLEGAL_RE.search(line):
        return []

    parts = [p.strip() for p in SPLIT_PROTOCOL_RE.split(line) if p.strip()]
    urls = [p for p in parts if re.match(
        r'^(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttp://|bchttps://|dht://|ptp://|ftp://|ws://|btsp://|btih://)',
        p, re.I
    )]
    return urls


def fetch_urls_from_source(url: str) -> Tuple[List[str], bool, str]:
    """抓取单个 http/https 上游源，解析其文本中的 Tracker URL。"""
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=TIMEOUT, verify=False)
            resp.raise_for_status()
            lines: List[str] = []
            for raw in resp.text.splitlines():
                urls = split_line_urls(raw)
                if urls:
                    lines.extend(urls)
            return lines, True, ""
        except requests.Timeout:
            error = f"超时 {TIMEOUT}秒 (尝试 {attempt+1}/{MAX_RETRIES})"
        except requests.HTTPError as e:
            error = f"HTTP错误: {e.response.status_code} (尝试 {attempt+1}/{MAX_RETRIES})"
        except requests.ConnectionError:
            error = f"连接错误 (DNS或网络问题) (尝试 {attempt+1}/{MAX_RETRIES})"
        except Exception as e:
            error = f"意外错误: {str(e)} (尝试 {attempt+1}/{MAX_RETRIES})"
    print(f"⚠ 警告: 无法拉取 {url}: {error}")
    return [], False, f"{url} | {error}"


def test_alive(url: str) -> bool:
    """可选 URL 可用性验证。"""
    if not CHECK_URL_ALIVE:
        return True

    parsed = urlsplit(url)
    if parsed.scheme in ("udp", "ltseed", "bcudp", "bchttp", "bchttps", "dht", "ptp", "btsp", "btih"):
        return True  # UDP / 私有协议暂时直接认为可用

    try:
        resp = requests.head(url, timeout=3, allow_redirects=True, verify=False)
        return resp.status_code < 400
    except:
        return False

# -------------------------------
# 主流程
# -------------------------------
def main() -> None:
    try:
        with open(SOURCES, encoding='utf-8') as f:
            source_items: List[str] = []
            for raw in f:
                source_items.extend(split_line_urls(raw))
        print(f"ℹ 信息: 从 {os.path.abspath(SOURCES)} 读取 {SOURCES}")
    except FileNotFoundError:
        raise RuntimeError(f"❌ {SOURCES} 文件未找到")
    except Exception as e:
        raise RuntimeError(f"❌ 读取 {SOURCES} 失败: {str(e)}")

    if not source_items:
        raise RuntimeError("❌ sources.list 为空或无有效 URL")

    upstreams = [u for u in source_items if urlsplit(u).scheme.lower() in ("http", "https")]
    direct_candidates = [u for u in source_items if urlsplit(u).scheme.lower() not in ("http", "https")]
    print(f"✅ 分类完成：上游 {len(upstreams)} 条，直接候选 {len(direct_candidates)} 条")

    all_urls: List[str] = []
    bad_sources: List[str] = []
    for src in upstreams:
        urls, success, error = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(error)

    all_urls.extend(direct_candidates)
    print(f"✅ 成功拉取 {len(all_urls)} 条 URL 🎉")

    deduped = [u for u in dict.fromkeys(all_urls).keys() if u.strip()]
    supported = [u for u in deduped if urlsplit(u).scheme.lower() in SUPPORTED_SCHEMES]
    print(f"ℹ 信息: 收集到 {len(supported)} 条唯一 URL")

    if not supported and bad_sources:
        raise RuntimeError("❌ 所有源均无法访问，无有效 Tracker")

    grouped = {scheme: [] for scheme in SCHEME_ORDER}
    for u in supported:
        scheme = urlsplit(u).scheme.lower()
        if scheme in grouped:
            grouped[scheme].append(u)
    for scheme in grouped:
        grouped[scheme].sort()

    ordered_output: List[str] = []
    for scheme in SCHEME_ORDER:
        ordered_output.extend(grouped[scheme])

    try:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"❌ 创建输出目录失败: {str(e)}")

    # 验证 URL 可用性（可选）
    final_urls = [u for u in ordered_output if test_alive(u)]

    if final_urls:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_urls) + '\n')
        print(f"✅ 成功写入 {len(final_urls)} 条 URL 到 {os.path.abspath(OUTPUT)} 🎉")
    else:
        print("ℹ 信息: 可用条目为空，未写入 tracker.txt")

    if bad_sources:
        with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad_sources) + '\n')
        print(f"⚠ 警告: {len(bad_sources)} 个源无法访问，已写入 {os.path.abspath(BAD_OUTPUT)}")
    else:
        print("ℹ 信息: 无失败源，未生成 bad_tracker.txt")


if __name__ == '__main__':
    main()