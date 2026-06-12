r = open('D:/tokai/server_fixed2.html', 'r', encoding='utf-8').read()

# Check nav section
nav_start = r.find('<nav class="nav"')
nav_end = r.find('</nav>', nav_start) + 6
nav = r[nav_start:nav_end]

print("=== NAV HTML (first 2500 chars) ===")
print(nav[:2500])

print("\n=== 检查语言按钮 ===")
for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
    count = r.count(f"setLang('{lang}')")
    print(f"setLang('{lang}'): {count}x")

print(f"\nid='settingsDropdown': {'YES' if 'id=\"settingsDropdown\"' in r else 'NO'}")
print(f"settings-dropdown class: {'YES' if 'class=\"settings-dropdown\"' in r else 'NO'}")

# Check setLang function
js = r[r.find('<script>')+8:r.rfind('</script>')]
setlang_start = js.find('function setLang')
if setlang_start >= 0:
    setlang_end = js.find('\n    function', setlang_start+1)
    if setlang_end < 0:
        setlang_end = setlang_start + 500
    print(f"\n=== setLang function ===")
    print(js[setlang_start:setlang_end])
