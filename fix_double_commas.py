import re

with open('D:/tokai/index-fixed3.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix: remove multiple consecutive commas (keep only one)
# Also fix trailing commas before }
fixed = re.sub(r',+', ',', html)
fixed = re.sub(r',\s*}', ' }', fixed)
fixed = re.sub(r',\s*\)', ' )', fixed)

# Count changes
diff = len(html) - len(fixed)
print(f"Removed {diff} extra comma characters")

# Save
with open('D:/tokai/index-fixed4.html', 'w', encoding='utf-8') as f:
    f.write(fixed)

# Extract JS
start = fixed.find('<script>')
end = fixed.rfind('</script>')
js = fixed[start+8:end]
with open('D:/tokai/check4.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f"HTML: {len(fixed)} bytes, JS: {len(js)} chars, braces: {js.count('{')}:{js.count('}')}")
