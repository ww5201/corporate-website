r = open('D:/tokai/server_fixed2.html', 'r', encoding='utf-8').read()

# Check nav section
nav_start = r.find('<nav class="nav"')
nav_end = r.find('</nav>', nav_start) + 6
nav = r[nav_start:nav_end]

with open('D:/tokai/nav_check.txt', 'w', encoding='utf-8') as f:
    f.write("=== NAV HTML ===\n")
    f.write(nav[:2500])
    f.write("\n\n=== 检查语言按钮 ===\n")
    for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
        count = r.count(f"setLang('{lang}')")
        f.write(f"setLang('{lang}'): {count}x\n")
    f.write(f"\nid='settingsDropdown': {'YES' if 'id=\"settingsDropdown\"' in r else 'NO'}\n")
    f.write(f"settings-dropdown class: {'YES' if 'class=\"settings-dropdown\"' in r else 'NO'}\n")
    
    # Check setLang function
    js = r[r.find('<script>')+8:r.rfind('</script>')]
    setlang_start = js.find('function setLang')
    if setlang_start >= 0:
        setlang_end = js.find('\n    function', setlang_start+1)
        if setlang_end < 0:
            setlang_end = setlang_start + 500
        f.write(f"\n=== setLang function ===\n")
        f.write(js[setlang_start:setlang_end])

print("Written to D:/tokai/nav_check.txt")
