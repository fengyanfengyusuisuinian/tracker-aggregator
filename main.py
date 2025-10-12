#!/usr/bin/env python3
import re, os, hashlib, requests
SOURCES = 'sources.list'
OUTPUT  = 'tracker.txt'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
def domain_set(url: str) -> set[str]:
    try:
        text = requests.get(url, headers=HEADERS, timeout=30).text
    except:
        return set()
    hosts = re.findall(r'(?i)([a-z0-9\-\.]+\.[a-z]{2,})(?=:\d+|$)', text)
    return {h.lower() for h in hosts}
def main():
    with open(SOURCES, encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    total = set().union(*map(domain_set, urls))
    old_hash = hashlib.sha256(open(OUTPUT, 'rb').read()).hexdigest() if os.path.exists(OUTPUT) else ''
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(total)) + '\n')
    new_hash = hashlib.sha256(open(OUTPUT, 'rb').read()).hexdigest()
    if old_hash == new_hash:
        print('No change.')
if __name__ == '__main__':
    main()
