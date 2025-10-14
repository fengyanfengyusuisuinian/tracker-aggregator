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
            error = f"Timeout after {TIMEOUT} seconds (attempt {attempt+1}/{MAX_RETRIES})"
        except requests.HTTPError as e:
            error = f"HTTP error: {e.response.status_code} (attempt {attempt+1}/{MAX_RETRIES})"
        except requests.ConnectionError:
            error = f"Connection error (DNS or network issue) (attempt {attempt+1}/{MAX_RETRIES})"
        except Exception as e:
            error = f"Unexpected error: {str(e)} (attempt {attempt+1}/{MAX_RETRIES})"
    
    print(f"Warning: Failed to fetch {url}: {error}")
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
        print(f"Info: Read {SOURCES} from {os.path.abspath(SOURCES)}")
    except FileNotFoundError:
        print(f"Error: {SOURCES} file not found")
        raise
    except Exception as e:
        print(f"Error: Failed to read {SOURCES}: {str(e)}")
        raise

    # Check if source list is empty
    if not source_urls:
        print("Error: sources.list is empty or contains no valid URLs")
        raise RuntimeError("No valid URLs in sources.list")

    # Fetch Trackers from each source
    for src in source_urls:
        urls, success, error = fetch_urls_from_source(src)
        if success:
            all_urls.extend(urls)
        else:
            bad_sources.append(error)

    # Deduplicate and sort (using dict.fromkeys for efficiency)
    unique_urls = sorted(dict.fromkeys(all_urls))
    print(f"Info: Collected {len(unique_urls)} unique URLs")

    # Check if all sources failed
    if not unique_urls and bad_sources:
        print("Error: All sources failed, no valid Trackers collected")
        raise RuntimeError("No valid Trackers collected")

    # Ensure output directory exists
    try:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        print(f"Info: Output directory created at {os.path.abspath(os.path.dirname(OUTPUT))}")
    except Exception as e:
        print(f"Error: Failed to create output directory {os.path.dirname(OUTPUT)}: {str(e)}")
        raise

    # Write tracker.txt
    try:
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_urls) + '\n')
        print(f"Success: Wrote {len(unique_urls)} URLs to {os.path.abspath(OUTPUT)}")
    except Exception as e:
        print(f"Error: Failed to write {OUTPUT}: {str(e)}")
        raise

    # Write bad_tracker.txt (only if there are failed sources)
    if bad_sources:
        try:
            with open(BAD_OUTPUT, 'w', encoding='utf-8') as f:
                f.write('\n'.join(bad_sources) + '\n')
            print(f"Warning: {len(bad_sources)} sources failed, wrote to {os.path.abspath(BAD_OUTPUT)}")
        except Exception as e:
            print(f"Error: Failed to write {BAD_OUTPUT}: {str(e)}")
            raise
    else:
        print("Info: No failed sources, bad_tracker.txt not generated")

if __name__ == '__main__':
    main()