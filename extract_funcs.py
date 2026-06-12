r = open('D:/tokai/server_current.html', 'r', encoding='utf-8').read()
js = r[r.find('<script>')+8:r.rfind('</script>')]
lines = js.split('\n')

# Find setLang function
for i, line in enumerate(lines):
    if 'function setLang' in line:
        with open('D:/tokai/setlang_func.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines[i:i+30]))
        print(f'setLang at line {i+1}')
        break

# Find startup
for i, line in enumerate(lines):
    if '启动' in line:
        with open('D:/tokai/startup_now.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines[i:]))
        print(f'Startup at line {i+1}')
        break

# Find toggleSettings
for i, line in enumerate(lines):
    if 'function toggleSettings' in line:
        with open('D:/tokai/toggle_func.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines[i:i+15]))
        print(f'toggleSettings at line {i+1}')
        break

# Check for currentLangLabel
for i, line in enumerate(lines):
    if 'currentLangLabel' in line and '//' not in line.strip():
        print(f"WARNING: currentLangLabel still at line {i+1}: {line.strip()[:100]}")

# Check for settings-menu
for i, line in enumerate(lines):
    if '.settings-menu' in line:
        print(f"WARNING: .settings-menu at line {i+1}: {line.strip()[:100]}")
