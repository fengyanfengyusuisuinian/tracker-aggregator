#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracker 聚合脚本（分组+直接候选支持）
功能：
1) 从 sources.list 读取源，支持一行多地址按协议切分
2) http/https 作为“上游列表”抓取并解析；非 http(s) 作为“直接候选”直接纳入
3) 正则切分支持：udp:// http:// https:// wss:// ltseed:// bcudp:// bchttp:// bchttps://
4) 使用 dict.fromkeys 去重；过滤空白与不支持协议
5) 按协议头分组，组内字典序输出；固定协议顺序
6) 失败上游写入 bad_tracker.txt（仅当存在失败），避免生成空的 tracker.txt
7) 上游失败重试 3 次；关键错误抛异常（缺文件、全部上游失败等）
"""

import os
import re
from urllib.parse import urlsplit
from typing import List, Tuple
import requests

# -------------------------------
# 常量配置
# -------------------------------

SOURCES = 'sources.list'                        # 上游列表文件（根目录）
OUTPUT = 'TrackerServer/tracker.txt'           # 可用 Tracker 输出文件
BAD_OUTPUT = 'TrackerServer/bad_tracker.txt'   # 失败上游输出文件
TIMEOUT = 10                                   # 请求超时（秒）
MAX_RETRIES = 3                                # 最大重试次数

# 支持协议与输出顺序
SUPPORTED_SCHEMES = ("http", "https", "udp", "wss", "ltseed", "bcudp", "bchttp", "bchttps")
SCHEME_ORDER = ["http", "https", "udp", "wss", "ltseed", "bcudp", "bchttp", "bchttps"]

# 按协议切分一行中多个 URL（正向前瞻）
SPLIT_PROTOCOL_RE = re.compile(
    r'(?=(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttps?://))',
    re.IGNORECASE
)

# -------------------------------
# 工具函数
# -------------------------------

def split_line_urls(line: str) -> List[str]:
    """按协议切分一行文本里的多个 URL，忽略 # 注释与空白。"""
    line = line.split('#', 1)[0].strip()
    if not line:
        return []
    parts = [p.strip() for p in SPLIT_PROTOCOL_RE.split(line) if p.strip()]
    urls = [p for p in parts if re.match(r'^(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttps?://)', p, re.I)]
    return urls

def fetch_urls_from_source(url: str) -> Tuple[List[str], bool, str]:
    """
    抓取单个 http/https 上游源，解析其文本中的 Tracker URL。
    返回: (urls, success, error_message)
    """
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=TIMEOUT)
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

# -------------------------------
# 主流程
# -------------------------------

def main() -> None:
    # 读取 sources.list，并按协议切分（支持一行多地址）
    try:
        with open(SOURCES, encoding='utf-8') as f:
            source_items: List[str] = []
            for raw in f:
                source_items.extend(split_line_urls(raw))
        print(f"ℹ 信息: 从 {os.path.abspath(SOURCES)} 读取 {SOURCES}")
    except FileNotFoundError:
        print(f"❌ 错误: {SOURCES} 文件未找到")
        raise
    except Exception as e:
        print(f"❌ 错误: 读取 {SOURCES} 失败: {str(e)}")
        raise

    # 校验是否读到任何地址
    if not source_items:
        print("❌ 错误: sources.list 为空或无有效 URL")
        raise RuntimeError("No valid URLs in sources.list")

    # 按是否为 http(s) 分类：上游列表 vs 直接候选
    upstreams = [u for u in source_items if urlsplit(u).scheme.lower() in ("http", "https")]
    direct_candidates = [u for u in source_items if urlsplit(u).scheme.lower() not in ("http", "https")]
    print(f"✅ 分类完成：上游 {len(upstreams)} 条，直接候选 {len(direct_candidates)} 条")

    # 抓取上游并汇总（不含去重）
    all_urls: List[str] = []
    bad_sources: List[str] = []
    for src in upstreams:
        urls, success, error = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(error)

    # 将非 http(s) 的直接候选一并纳入
    all_urls.extend(direct_candidates)

    # 记录抓取到的总量（去重前）
    print(f"✅ 成功拉取 {len(all_urls)} 条 URL 🎉")

    # 去重 + 过滤空白 + 过滤不支持协议（保持原始出现顺序）
    deduped = [u for u in dict.fromkeys(all_urls).keys() if u.strip()]
    supported = [u for u in deduped if urlsplit(u).scheme.lower() in SUPPORTED_SCHEMES]
    print(f"ℹ 信息: 收集到 {len(supported)} 条唯一 URL")

    # 若完全没有收集到，且存在失败上游 → 视为关键错误
    if not supported and bad_sources:
        print("❌ 错误: 所有源均无法访问，无有效 Tracker")
        raise RuntimeError("No valid Trackers collected")

    # 按协议分组 → 组内字典序排序 → 按固定协议顺序拼接
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

    # 确保输出目录存在
    try:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        print(f"ℹ 信息: 输出目录创建于 {os.path.abspath(os.path.dirname(OUTPUT))}")
    except Exception as e:
        print(f"❌ 错误: 创建输出目录 {os.path.dirname(OUTPUT)} 失败: {str(e)}")
        raise

    # 写入 tracker.txt（仅当非空，避免生成空文件）
    if ordered_output:
        try:
            with open(OUTPUT, 'w', encoding='utf-8') as f:
                f.write('\n'.join(ordered_output) + '\n')
            print(f"✅ 成功写入 {len(ordered_output)} 条 URL 到 {os.path.abspath(OUTPUT)} 🎉")
        except Exception as e:
            print(f"❌ 错误: 写入 {OUTPUT} 失败: {str(e)}")
            raise
    else:
        print("ℹ 信息: 可用条目为空，未写入 tracker.txt")

    # 写入 bad_tracker.txt（仅当存在失败上游）
    if bad_sources:
        try:
            with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
                f.write('\n'.join(bad_sources) + '\n')
            print(f"⚠ 警告: {len(bad_sources)} 个源无法访问，已写入 {os.path.abspath(BAD_OUTPUT)}")
        except Exception as e:
            print(f"❌ 错误: 写入 {BAD_OUTPUT} 失败: {str(e)}")
            raise
    else:
        print("ℹ 信息: 无失败源，未生成 bad_tracker.txt")

if __name__ == '__main__':
    main()
