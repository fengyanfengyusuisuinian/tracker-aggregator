#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracker聚合脚本 - 只改顺序版
处理顺序：合并 → 去重 → 存活检测 → 排序
数据源逻辑完全不动
"""

import os
import re
from urllib.parse import urlsplit
from typing import List, Tuple
import requests

# 原始配置完全不动
SOURCES = 'sources.list'
OUTPUT = 'TrackerServer/tracker.txt'
BAD_OUTPUT = 'TrackerServer/bad_tracker.txt'
TIMEOUT = 10
MAX_RETRIES = 3
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
CHECK_URL_ALIVE = True
SPLIT_PROTOCOL_RE = re.compile(
    r'(?=(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttp://|bchttps://|dht://|ptp://|ftp://|ws://|btsp://|btih://))',
    re.IGNORECASE
)
ILLEGAL_RE = re.compile(
    r"(location\.protocol|nextChapterData|document\.|window\.|eval\(|\+.*[\'\"]|[\'\"]\+|return url|var |function\()",
    re.I
)

# 原始函数完全不动
def split_line_urls(line: str) -> List[str]:
    line = line.split('#', 1)[0].strip()
    if not line or ILLEGAL_RE.search(line):
        return []
    parts = [p.strip() for p in SPLIT_PROTOCOL_RE.split(line) if p.strip()]
    return [p for p in parts if re.match(
        r'^(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttp://|bchttps://|dht://|ptp://|ftp://|ws://|btsp://|btih://)',
        p, re.I
    )]

def fetch_urls_from_source(url: str) -> Tuple[List[str], bool, str]:
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
    if not CHECK_URL_ALIVE:
        return True
    parsed = urlsplit(url)
    if parsed.scheme in ("udp", "ltseed", "bcudp", "bchttp", "bchttps", "dht", "ptp", "btsp", "btih"):
        return True
    try:
        resp = requests.head(url, timeout=3, allow_redirects=True, verify=False)
        return resp.status_code < 400
    except:
        return False

# 主函数只改顺序，其他不动
def main():
    try:
        # 1. 读取sources.list（数据源URL列表）
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

    # 2. 原始分类逻辑不动
    upstreams = [u for u in source_items if urlsplit(u).scheme.lower() in ("http", "https")]
    direct_candidates = [u for u in source_items if urlsplit(u).scheme.lower() not in ("http", "https")]
    print(f"✅ 分类完成：上游 {len(upstreams)} 条，直接候选 {len(direct_candidates)} 条")

    # 3. 抓取上游源
    all_urls: List[str] = []
    bad_sources: List[str] = []
    for src in upstreams:
        urls, success, error = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(error)

    # 4. 合并所有抓取结果 + 直接候选
    all_urls.extend(direct_candidates)
    print(f"✅ 合并完成，共 {len(all_urls)} 条 URL")

    # 5. 去重（保持原始dict.fromkeys方式）
    deduped = [u for u in dict.fromkeys(all_urls).keys() if u.strip()]
    supported = [u for u in deduped if urlsplit(u).scheme.lower() in SUPPORTED_SCHEMES]
    print(f"ℹ 信息: 去重后 {len(supported)} 条有效 URL")

    # 6. 存活检测（如果开启）
    if CHECK_URL_ALIVE:
        print(f"🔍 开始存活检测...")
        final_urls = [u for u in supported if test_alive(u)]
        print(f"✅ 存活检测完成: {len(final_urls)}/{len(supported)} 个可用")
    else:
        final_urls = supported
        print(f"ℹ️  跳过存活检测，使用全部 {len(final_urls)} 个URL")

    # 7. 最后排序：按协议优先级
    grouped = {scheme: [] for scheme in SCHEME_ORDER}
    for u in final_urls:
        scheme = urlsplit(u).scheme.lower()
        if scheme in grouped:
            grouped[scheme].append(u)
    
    # 按SCHEME_ORDER顺序输出，同协议内按字母排序
    ordered_output: List[str] = []
    for scheme in SCHEME_ORDER:
        grouped[scheme].sort()
        ordered_output.extend(grouped[scheme])

    # 8. 输出文件（路径和格式完全不动）
    try:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"❌ 创建输出目录失败: {str(e)}")

    if ordered_output:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ordered_output) + '\n')
        print(f"✅ 成功写入 {len(ordered_output)} 条 URL 到 {os.path.abspath(OUTPUT)}")
    else:
        print("ℹ 信息: 可用条目为空，未写入 tracker.txt")

    # 错误源报告（完全不动）
    if bad_sources:
        with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad_sources) + '\n')
        print(f"⚠ 警告: {len(bad_sources)} 个源无法访问，已写入 {os.path.abspath(BAD_OUTPUT)}")
    else:
        print("ℹ 信息: 无失败源，未生成 bad_tracker.txt")


if __name__ == '__main__':
    main()
