with open(r'D:\tokai\src\main.js', 'r', encoding='utf-8') as f:
    content = f.read()
old = '  applyLang(currentLang);\n  console.log'
new = '  applyLang(currentLang);\n  loadShopProducts();\n  console.log'
if old in content:
    content = content.replace(old, new, 1)
    with open(r'D:\tokai\src\main.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: added loadShopProducts()')
else:
    print('NOT FOUND: pattern not matched')
