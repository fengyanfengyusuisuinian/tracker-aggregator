#!/usr/bin/env python3
"""
Tracker 域名聚合脚本
下载 sources.list 里的所有 URL → 提取 host → 去重排序
输出到 TrackerServer/tracker.txt
"""
import re, os, requests

# 源 URL 列表文件
SOURCES = 'sources.list'
# 输出文件路径（无空格目录）
OUTPUT = 'TrackerServer/tracker.txt'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def domain_set(url: str) -> set[str]:
    """从单个 URL 提取域名集合"""
    try:
        text = requests.get(url, headers=HEADERS, timeout=30).text
    except Exception as e:
        print(f'WARN: {url} 下载失败 {e}')
        return set()
    # 匹配 host:port 或纯 host
    hosts = re.findall(r'(?i)([a-z0-9\-\.]+\.[a-z]{2,})(?=:\d+|$)', text)
    return {h.lower() for h in hosts}

def main():
    # 读取 sources.list
    with open(SOURCES, encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # 聚合去重
    total = set().union(*map(domain_set, urls))

    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # 写入排序结果
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(total)) + '\n')

    # 打印日志：已写入条目数
    print(f'✅ 已写入 {len(total)} 条域名到 {OUTPUT}')

if __name__ == '__main__':
    main()
