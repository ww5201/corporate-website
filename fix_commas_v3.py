import re

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Strategy: find places where a closing single-quote is followed directly by newline
# and then whitespace + identifier: (meaning missing comma)
# Pattern: 'value'\n  key: (but NOT 'value',\n  key:)
# Use: replace '\n' with ',\n' when preceded by ' and followed by spaces + identifier

# First, let's find all occurrences
matches = list(re.finditer(r"'(\n(\s+)[a-z_][a-z_0-9]*:)", html))
print(f"Found {len(matches)} potential missing commas")

# Check each match
fixes = []
for m in matches:
    pos = m.start()
    # The ' is at pos, the \n is at pos+1
    # Check if there's a comma before the '
    if pos > 0 and html[pos-1] == ',':
        continue  # already has comma
    fixes.append(pos)

print(f"Need to fix: {len(fixes)} positions")

# Apply fixes in reverse order to preserve positions
fixed = html
for pos in reversed(fixes):
    # Insert comma after the ' at pos
    fixed = fixed[:pos+1] + ',' + fixed[pos+1:]

print(f"Before: {len(html)} bytes")
print(f"After: {len(fixed)} bytes (+{len(fixed)-len(html)} commas)")

# Save
with open('D:/tokai/index-fixed3.html', 'w', encoding='utf-8') as f:
    f.write(fixed)

# Validate
start = fixed.find('<script>')
end = fixed.rfind('</script>')
js = fixed[start+8:end]
with open('D:/tokai/check3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print(f"JS: {len(js)} chars, braces: {js.count('{')}:{js.count('}')}")
