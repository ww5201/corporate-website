import re

with open(r'D:\tokai\index-final.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find settingsDropdown references
for i, line in enumerate(html.split('\n'), 1):
    if 'settingsDropdown' in line or 'settings-dropdown' in line or 'toggleSettings' in line:
        print(f"{i}: {line.strip()[:120]}")

# Find lang-switch, lang-toggle, lang-dropdown references
print("\n--- Lang references ---")
for i, line in enumerate(html.split('\n'), 1):
    if 'lang-switch' in line or 'lang-toggle' in line or 'lang-dropdown' in line or 'toggleLangMenu' in line:
        print(f"{i}: {line.strip()[:120]}")
