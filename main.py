#!/usr/bin/env python3
"""
Tracker URL 聚合脚本（优化版）
功能：
1. 从 sources.list 读取 Tracker 源 URL
2. 抓取每个源的 Tracker 列表，去重（用 dict.fromkeys 优化内存）并排序
3. 无法访问的源记录到 bad_tracker.txt（包含错误原因）
4. 自动拆分同一行多个 URL
5. 网络请求失败时重试 3 次
6. 关键错误（如文件缺失、全源失败、失败比例过高）抛出异常，确保 GitHub Actions 标记失败
7. 调试输出实际文件路径，确认生成位置
输出：
- TrackerServer/tracker.txt：去重排序后的 Tracker 列表
- TrackerServer/bad_tracker.txt：失败的源 URL 和错误原因
"""

import os
import re
import requests
from typing import List, Tuple

# 常量定义
SOURCES = 'sources.list'  # 源文件路径（根目录）
OUTPUT = 'TrackerServer/tracker.txt'  # 输出 Tracker 文件
BAD_OUTPUT = 'TrackerServer/bad_tracker.txt'  # 失败源输出文件
TIMEOUT = 10  # 每个请求的超时时间（秒）
MAX_RETRIES = 3  # 最大重试次数

def fetch_urls_from_source(url: str) -> Tuple[List[str], bool, str]:
    """
    抓取单个源 URL 的 Tracker 列表
    参数：
        url: 源 URL（字符串）
    返回：
        Tuple[List[str], bool, str]: (抓取到的 Tracker 列表, 是否成功, 错误信息)
    """
    for attempt in range(MAX_RETRIES):  # 重试 3 次
        try:
            # 发送 HTTP 请求，设置超时
            resp = requests.get(url, timeout=TIMEOUT)
            resp.raise_for_status()  # 检查 HTTP 状态码
            lines = []
            # 逐行处理响应，过滤空行和注释
            for line in resp.text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # 按协议（http://, https://, udp://）拆分多条 URL
                lines.extend(re.split(r'(?=https?://|udp://)', line))
            return lines, True, ""
        except requests.Timeout:
            error = f"Timeout after {TIMEOUT}s (attempt {attempt+1}/{MAX_RETRIES})"
        except requests.HTTPError as e:
            error = f"HTTP error: {e.response.status_code} (attempt {attempt+1}/{MAX_RETRIES})"
        except requests.ConnectionError:
            error = f"Connection error (DNS or network issue) (attempt {attempt+1}/{MAX_RETRIES})"
        except Exception as e:
            error = f"Unexpected error: {str(e)} (attempt {attempt+1}/{MAX_RETRIES})"
    
    # 所有重试失败后，记录错误
    print(f"WARN: {url} 下载失败: {error}")
    return [], False, f"{url} | {error}"

def main() -> None:
    """
    主函数：读取源，抓取 Tracker，去重排序，写入输出文件
    如果关键步骤失败，抛出异常，确保 GitHub Actions 标记失败
    """
    # 打印当前工作目录，调试用
    print(f"DEBUG: Current working directory: {os.getcwd()}")

    all_urls: List[str] = []  # 存储所有 Tracker URL
    bad_sources: List[str] = []  # 存储失败的源和错误信息

    # 读取 sources.list
    try:
        with open(SOURCES, encoding='utf-8') as f:
            source_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"DEBUG: Reading {SOURCES} from {os.path.abspath(SOURCES)}")
    except FileNotFoundError:
        print(f"ERROR: {SOURCES} 文件未找到")
        raise  # 抛出异常，让 Actions 失败
    except Exception as e:
        print(f"ERROR: 读取 {SOURCES} 失败: {str(e)}")
        raise

    # 检查源列表是否为空
    if not source_urls:
        print("ERROR: sources.list 为空或无有效 URL")
        raise RuntimeError("No valid URLs in sources.list")

    # 抓取每个源的 Tracker
    for src in source_urls:
        urls, success, error = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(error)

    # 去重并排序（使用 dict.fromkeys 优化内存）
    unique_urls = sorted(dict.fromkeys(all_urls))  # dict.fromkeys 去重，sorted 排序
    print(f"DEBUG: Collected {len(unique_urls)} unique URLs")

    # 检查是否所有源都失败
    if not unique_urls and bad_sources:
        print("ERROR: 所有源都无法访问，无有效 Tracker")
        raise RuntimeError("No valid trackers collected")

    # 检查失败比例
    if bad_sources and len(bad_sources) / len(source_urls) > 0.5:  # 超50%源失败
        print(f"ERROR: {len(bad_sources)}/{len(source_urls)} 源失败，建议检查 sources.list")
        raise RuntimeError("Too many sources failed")

    # 确保输出目录存在
    try:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        print(f"DEBUG: Output directory created at {os.path.abspath(os.path.dirname(OUTPUT))}")
    except Exception as e:
        print(f"ERROR: 创建输出目录 {os.path.dirname(OUTPUT)} 失败: {str(e)}")
        raise

    # 写入 tracker.txt
    try:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_urls) + '\n')
        print(f"✅ 已写入 {len(unique_urls)} 条 URL 到 {os.path.abspath(OUTPUT)}")
    except Exception as e:
        print(f"ERROR: 写入 {OUTPUT} 失败: {str(e)}")
        raise

    # 写入 bad_tracker.txt（如果有失败源）
    if bad_sources:
        try:
            with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
                f.write('\n'.join(bad_sources) + '\n')
            print(f"⚠ {len(bad_sources)} 个源无法访问，已写入 {os.path.abspath(BAD_OUTPUT)}")
        except Exception as e:
            print(f"ERROR: 写入 {BAD_OUTPUT} 失败: {str(e)}")
            raise

if __name__ == '__main__':
    main()