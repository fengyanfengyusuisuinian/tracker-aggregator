#!/usr/bin/env python3
"""
Tracker URL aggregation script (optimized)
Features:
1. Read Tracker source URLs from sources.list
2. Fetch Tracker lists, deduplicate using dict.fromkeys for memory efficiency, and sort
3. Record failed sources to bad_tracker.txt (only if failures exist)
4. Split multiple URLs in a line by protocol (http://, https://, udp://)
5. Retry failed requests 3 times
6. Raise exceptions for critical errors (e.g., missing file, all sources failed)
7. Log the number of fetched URLs before deduplication with Chinese messages and emojis
Outputs:
- TrackerServer/tracker.txt: Deduplicated and sorted Tracker list
- TrackerServer/bad_tracker.txt: Failed source URLs and error reasons (only if failures)
"""

import os
import re
import requests
from typing import List, Tuple

# Constants
SOURCES = 'sources.list'  # Source file path (root directory)
OUTPUT = 'TrackerServer/tracker.txt'  # Output Tracker file
BAD_OUTPUT = 'TrackerServer/bad_tracker.txt'  # Failed sources output file
TIMEOUT = 10  # Request timeout in seconds
MAX_RETRIES = 3  # Max retry attempts

def fetch_urls_from_source(url: str) -> Tuple[List[str], bool, str]:
    """
    Fetch Tracker list from a single source URL
    Args:
        url: Source URL (string)
    Returns:
        Tuple[List[str], bool, str]: (Fetched Tracker URLs, success status, error message)
    """
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            lines = []
            for line in resp.text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Split by protocol to separate multiple Tracker URLs in a single line
                urls = re.split(r'(?=https?://|udp://)', line)
                lines.extend([url for url in urls if url.strip()])
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

def main() -> None:
    """
    Main function: Read sources, fetch Trackers, deduplicate, sort, and write output files
    Raises exceptions for critical failures to mark GitHub Actions as failed
    """
    all_urls: List[str] = []
    bad_sources: List[str] = []

    # Read sources.list
    try:
        with open(SOURCES, encoding='utf-8') as f:
            source_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"ℹ 信息: 从 {os.path.abspath(SOURCES)} 读取 {SOURCES}")
    except FileNotFoundError:
        print(f"❌ 错误: {SOURCES} 文件未找到")
        raise
    except Exception as e:
        print(f"❌ 错误: 读取 {SOURCES} 失败: {str(e)}")
        raise

    # Check if source list is empty
    if not source_urls:
        print("❌ 错误: sources.list 为空或无有效 URL")
        raise RuntimeError("No valid URLs in sources.list")

    # Fetch Trackers from each source
    for src in source_urls:
        urls, success, error = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(error)

    # Log the number of fetched URLs (before deduplication)
    print(f"✅ 成功拉取 {len(all_urls)} 条 URL 🎉")

    # Deduplicate and sort (using dict.fromkeys for efficiency)
    unique_urls = sorted(dict.fromkeys(all_urls))
    print(f"ℹ 信息: 收集到 {len(unique_urls)} 条唯一 URL")

    # Check if all sources failed
    if not unique_urls and bad_sources:
        print("❌ 错误: 所有源均无法访问，无有效 Tracker")
        raise RuntimeError("No valid Trackers collected")

    # Ensure output directory exists
    try:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        print(f"ℹ 信息: 输出目录创建于 {os.path.abspath(os.path.dirname(OUTPUT))}")
    except Exception as e:
        print(f"❌ 错误: 创建输出目录 {os.path.dirname(OUTPUT)} 失败: {str(e)}")
        raise

    # Write tracker.txt
    try:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_urls) + '\n')
        print(f"✅ 成功写入 {len(unique_urls)} 条 URL 到 {os.path.abspath(OUTPUT)} 🎉")
    except Exception as e:
        print(f"❌ 错误: 写入 {OUTPUT} 失败: {str(e)}")
        raise

    # Write bad_tracker.txt (only if there are failed sources)
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