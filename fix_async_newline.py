import re

with open('D:/tokai/index-fixed-final.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Before: {len(html)} bytes")

# Fix: remove blank lines between 'async' and 'function'
# Pattern: 'async \n\n  function' -> 'async function'
html = re.sub(r'async\s+\n\s*\n\s*function', 'async function', html)

# Also fix any other similar blank-line issues in function declarations
# Pattern: 'return \n\n  value' (unlikely but just in case)
# html = re.sub(r'return\s+\n\s*\n', 'return ', html)

with open('D:/tokai/index-fixed-final.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"After: {len(html)} bytes")

# Validate JS
start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]
with open('D:/tokai/check-final.js', 'w', encoding='utf-8') as f:
    f.write(js)
print(f"JS: {len(js)} chars")
