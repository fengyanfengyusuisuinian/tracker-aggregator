#!/usr/bin/env python3
"""
Tracker URL 聚合脚本（最终版，支持 bad tracker 输出）
功能：
1. 保留原 URL
2. 去重 + 排序
3. 无法访问的源单独输出到 bad_tracker.txt
4. 自动拆分同一行多个 URL
输出：
- TrackerServer/tracker.txt
- TrackerServer/bad_tracker.txt
"""
import os
import re
import requests

SOURCES = 'sources.list'
OUTPUT = 'TrackerServer/tracker.txt'
BAD_OUTPUT = 'TrackerServer/bad_tracker.txt'
TIMEOUT = 10  # 秒

def fetch_urls_from_source(url):
    """抓取单个源 URL，如果失败返回空列表"""
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        lines = []
        for line in resp.text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 按协议拆分多条 URL
            lines.extend(re.split(r'(?=https?://|udp://)', line))
        return lines, True
    except Exception as e:
        print(f"WARN: {url} 下载失败: {e}")
        return [], False

def main():
    all_urls = []
    bad_sources = []

    # 读取 sources.list
    with open(SOURCES, encoding='utf-8') as f:
        source_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # 抓取每个源
    for src in source_urls:
        urls, success = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(src)

    # 去重 + 排序
    unique_urls = sorted(set(all_urls))

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # 写入 tracker.txt
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_urls) + '\n')

    print(f'✅ 已写入 {len(unique_urls)} 条 URL 到 {OUTPUT}')

    # 写入 bad_tracker.txt
    if bad_sources:
        with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad_sources) + '\n')
        print(f"⚠ {len(bad_sources)} 个源无法访问，已写入 {BAD_OUTPUT}")

if __name__ == '__main__':
    main()
