import re

with open('D:/tokai/index-fixed-final.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Before: {len(html)} bytes")

# Find the exact pattern
import subprocess
html = html.replace(
    "fetch(`${API}/products`)\n          fetch(`${API}/payment-config`)",
    "fetch(`${API}/products`),\n          fetch(`${API}/payment-config`)"
)

with open('D:/tokai/index-fixed-final.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"After: {len(html)} bytes")

# Extract JS
start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]
with open('D:/tokai/check-final2.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Validate with Node.js
result = subprocess.run(
    ['node', 'D:/tokai/validate_fix.js'],
    capture_output=True, text=True, timeout=10
)
print(result.stdout.strip())
if result.returncode != 0:
    print(result.stderr.strip())
