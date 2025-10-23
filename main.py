def split_line_urls(line: str) -> List[str]:
    """按协议切分一行文本里的多个 URL，忽略 # 注释与空白，并过滤 JS 拼接或乱码。"""
    line = line.split('#', 1)[0].strip()
    if not line:
        return []
    
    # 🧹 第一步：直接排除明显的网页脚本或拼接式垃圾行
    if any(k in line for k in [
        'location.protocol', 'nextChapterData', 'document.', 'window.', 'eval(',
        "' + '", '" + "', "+'", "'+", 'html;', 'return url', 'var ', 'function('
    ]):
        return []
    
    # 🪄 第二步：按协议切分
    parts = [p.strip() for p in SPLIT_PROTOCOL_RE.split(line) if p.strip()]
    
    # ✅ 只保留合法协议的 URL
    urls = [p for p in parts if re.match(
        r'^(?:https?://|udp://|wss://|ltseed://|bcudp://|bchttp://|bchttps://)', p, re.I)]
    
    # 🚫 再次保险过滤掉包含 JS 片段的内容
    urls = [p for p in urls if not re.search(
        r'(location\.protocol|nextChapterData|document\.|window\.|eval\(|\+.*[\'"]|[\'"]\+)', p, re.I)]
    
    return urls