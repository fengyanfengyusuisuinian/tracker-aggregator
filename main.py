#!/usr/bin/env python3
"""
Tracker URL 聚合脚本（优化版）
保留原始 URL 格式，只去重 + 排序
输出到 TrackerServer/tracker.txt
"""
import os

SOURCES = 'sources.list'
OUTPUT = 'TrackerServer/tracker.txt'

def main():
    # 读取源文件，每行保留原样
    with open(SOURCES, encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # 去重 + 排序
    unique_urls = sorted(set(urls))

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # 写入文件
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_urls) + '\n')

    print(f'✅ 已写入 {len(unique_urls)} 条 URL 到 {OUTPUT}')

if __name__ == '__main__':
    main()
