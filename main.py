#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracker聚合脚本 - 并发+超时+存活检测完整版
输出：
  trackers_merged.txt   合并+去重后完整列表
  trackers_alive.txt    通过存活检测的可用列表
  sources_failed.txt    数据源拉取失败记录
"""

import os
import re
import time
import requests
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

# ========== 配置 ==========
SOURCES = 'sources.list'
OUTPUT_DIR = 'TrackerServer'
OUTPUT = os.path.join(OUTPUT_DIR, 'tracker.txt')          # 兼容旧文件
BAD_OUTPUT = os.path.join(OUTPUT_DIR, 'bad_tracker.txt')  # 兼容旧文件

TIMEOUT = (5, 8)          # (连接, 读取) 秒
MAX_RETRIES = 2           # 数据源重试
MAX_WORKERS = 20          # 并发线程
CHECK_URL_ALIVE = True    # 启用存活检测！！！

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

# ========== 工具函数 ==========
def split_line_urls(line: str) -> List[str]:
    line = line.split('#', 1)[0].strip()
    if not line:
        return []
    parts = [p.strip() for p in re.split(r'(?=(?:https?://|udp://|wss?://|ltseed://|bcudp://|bchttp://|bchttps://|dht://|ptp://|ftp://|ws://|btsp://|btih://))', line, flags=re.I) if p.strip()]
    return [p for p in parts if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', p)]

def fetch_one_source(url: str) -> Tuple[str, List[str], str]:
    """并发抓取单个数据源，快速失败"""
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, timeout=TIMEOUT, verify=False, headers={'User-Agent': 'tracker-sub/1.0'})
            r.raise_for_status()
            lines = []
            for raw in r.text.splitlines():
                lines.extend(split_line_urls(raw))
            return url, lines, ""
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                return url, [], f"{url} | {e}"
            time.sleep(1)

def test_tracker_alive(url: str) -> bool:
    """单tracker存活检测，粗暴快速"""
    scheme = urlsplit(url).scheme.lower()
    if scheme == 'udp':
        # UDP 检测省略，直接视为存活
        return True
    try:
        r = requests.head(url, timeout=TIMEOUT, allow_redirects=True, verify=False, headers={'User-Agent': 'tracker-sub/1.0'})
        return r.status_code < 500
    except:
        return False

# ========== 主函数 ==========
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. 读取数据源列表
    with open(SOURCES, encoding='utf-8') as f:
        source_items = []
        for raw in f:
            source_items.extend(split_line_urls(raw))
    print(f'[INFO] 读取 {SOURCES} 完成，共 {len(source_items)} 条数据源')

    # 2. 并发抓取所有上游源
    upstreams = [u for u in source_items if urlsplit(u).scheme.lower() in ("http", "https")]
    direct = [u for u in source_items if urlsplit(u).scheme.lower() not in ("http", "https")]
    all_urls, bad_sources = [], []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        future_map = {ex.submit(fetch_one_source, u): u for u in upstreams}
        for f in as_completed(future_map):
            src, urls, err = f.result()
            if err:
                bad_sources.append(err)
            else:
                all_urls.extend(urls)
    all_urls.extend(direct)
    print(f'[INFO] 抓取完成，合并后 {len(all_urls)} 条 URL')

    # 3. 去重
    supported = [u for u in dict.fromkeys(all_urls) if u.strip() and urlsplit(u).scheme.lower() in SUPPORTED_SCHEMES]
    print(f'[INFO] 去重后 {len(supported)} 条有效 URL')

    # 4. 并发存活检测
    if CHECK_URL_ALIVE:
        print('[INFO] 开始并发存活检测...')
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            future_map = {ex.submit(test_tracker_alive, u): u for u in supported}
            alive = [f.result() for f in as_completed(future_map) if f.result()]
        print(f'[INFO] 存活检测完成：{len(alive)}/{len(supported)} 可用')
    else:
        alive = supported

    # 5. 按协议排序
    grouped = {s: [] for s in SCHEME_ORDER}
    for u in alive:
        grouped[urlsplit(u).scheme.lower()].append(u)
    ordered = []
    for s in SCHEME_ORDER:
        ordered.extend(sorted(grouped[s]))

    # 6. 输出三文件 + 兼容旧文件
    merged_file = os.path.join(OUTPUT_DIR, 'trackers_merged.txt')
    alive_file = os.path.join(OUTPUT_DIR, 'trackers_alive.txt')
    failed_file = os.path.join(OUTPUT_DIR, 'sources_failed.txt')

    with open(merged_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(supported) + '\n')
    print(f'[OUT] 未检测完整列表 → {merged_file}')

    if CHECK_URL_ALIVE:
        with open(alive_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ordered) + '\n')
        print(f'[OUT] 存活列表 → {alive_file}')

    if bad_sources:
        with open(failed_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad_sources) + '\n')
        print(f'[OUT] 失败源记录 → {failed_file}')

    # 兼容旧文件（供 GitHub Actions 提交用）
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ordered) + '\n')
    if bad_sources:
        with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad_sources) + '\n')

    print('[DONE] 全部完成！')


if __name__ == '__main__':
    main()
