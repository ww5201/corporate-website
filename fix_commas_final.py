import re

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Before: {len(html)} bytes")

# Better regex: match key: 'value' followed by newline+spaces+key: (including digits in keys)
# Pattern 1: : 'value'\n        nextKey:
fixed = re.sub(r"(:\s*'[^']+')(\n\s+[a-z_][a-z_0-9]*:)", r"\1,\2", html)

# Pattern 2: : "value"\n        nextKey: (double-quoted)
fixed = re.sub(r'(:\s*"[^"]+"\n\s+[a-z_][a-z_0-9]*:)', lambda m: m.group(0).replace('"\n', '",\n' if '",\n' not in m.group(0) else '"\n', 1), fixed)

# Count fixes
diff = len(fixed) - len(html)
print(f"After: {len(fixed)} bytes (+{diff} commas)")

# Write back
with open('D:/tokai/index-fixed3.html', 'w', encoding='utf-8') as f:
    f.write(fixed)

# Extract JS and validate
start = fixed.find('<script>')
end = fixed.rfind('</script>')
js = fixed[start+8:end]

# Write JS for Node.js validation
with open('D:/tokai/check3.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f"JS: {len(js)} chars")
print(f"Braces: {js.count('{')}:{js.count('}')}")
print("Done - check with Node.js next")
