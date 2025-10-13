#!/usr/bin/env python3
"""
Tracker URL 聚合脚本（最终版，支持 bad tracker 输出）
功能：
1. 保留原 URL
2. 去重 + 排序
3. 无法访问的源单独输出到 bad_tracker.txt
4. 自动拆分同一行任意合法协议头
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
TIMEOUT = 10  # 单次请求超时（秒）


def fetch_urls_from_source(url: str):
    """
    下载单个源内容
    返回 (urls_list, True)  下载成功
         ([], False)       任意异常（即无法访问）
    """
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        lines = []
        for line in resp.text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 拆分任意合法协议头（xxx://）
            lines.extend(re.split(r'(?=[^:\s]+://)', line))
        return lines, True
    except Exception as e:
        # 只要失败就把原 url 记入坏源列表，不再重试
        print(f"WARN: {url} 下载失败: {e}")
        return [], False


def dedup_exact(urls):
    """
    字符串完全相等去重
    区分大小写、协议、端口；保留首次出现顺序，最后统一排序
    """
    seen = set()
    out = []
    for u in urls:
        u = u.strip()
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return sorted(out)


def main():
    all_urls = []  # 所有成功抓到的原始行
    bad_sources = []  # 无法访问的源地址

    # 读取待抓取源列表
    with open(SOURCES, encoding='utf-8') as f:
        source_urls = [line.strip() for line in f
                       if line.strip() and not line.startswith('#')]

    # 逐源抓取
    for src in source_urls:
        urls, ok = fetch_urls_from_source(src)
        if ok:
            all_urls.extend(urls)
        else:
            bad_sources.append(src)

    # 去重 & 排序
    unique_urls = dedup_exact(all_urls)

    # 写结果
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_urls) + '\n')

    print(f'✅ 已写入 {len(unique_urls)} 条 URL 到 {OUTPUT}')

    # 写失败源
    if bad_sources:
        with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bad_sources) + '\n')
        print(f"⚠️  {len(bad_sources)} 个源无法访问，已写入 {BAD_OUTPUT}")


if __name__ == '__main__':
    main()
