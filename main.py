#!/usr/bin/env python3
"""
Tracker URL 聚合脚本（优化版）
保留原始 URL 格式，只去重 + 排序
输出到 TrackerServer/tracker.txt
"""
import os
import requests

SOURCES = 'sources.list'
OUTPUT = 'TrackerServer/tracker.txt'

def fetch_urls_from_source(url):
    """从单个源抓取 URL，每行保留原样"""
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        lines = [line.strip() for line in resp.text.splitlines() if line.strip() and not line.startswith('#')]
        return lines
    except Exception as e:
        print(f"WARN: {url} 下载失败: {e}")
        return []

def main():
    all_urls = []

    # 读取 sources.list 中的每个源 URL
    with open(SOURCES, encoding='utf-8') as f:
        source_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # 抓取每个源
    for src in source_urls:
        urls = fetch_urls_from_source(src)
        all_urls.extend(urls)

    # 去重 + 排序
    unique_urls = sorted(set(all_urls))

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # 写入 TrackerServer/tracker.txt
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_urls) + '\n')

    print(f'✅ 已写入 {len(unique_urls)} 条 URL 到 {OUTPUT}')

if __name__ == '__main__':
    main()
