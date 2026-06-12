import re

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Before: {len(html)} bytes")

# Only add comma where there is NO comma already
# Match: 'value' followed by newline and next key, but NOT if comma already present
# Negative lookbehind for comma: (?<!,)
fixed = re.sub(r"'([^']*)'(\n\s+[a-z_][a-z_0-9]*:)", lambda m: f"'{m.group(1)}',\n{m.group(2).lstrip()}" if not m.group(0).endswith("',\n") and not "'," in m.group(0)[-len(m.group(1))-5:] else m.group(0), html)

# Simpler approach: find all 'value'\n  key: patterns where value is NOT followed by comma
# Pattern: 'value' then newline then spaces then identifier:
# But NOT 'value',\n
fixed2 = html
count = 0
# Find positions where we need to add commas
pattern = re.compile(r"'([^']*)'\n(\s+[a-z_][a-z_0-9]*:)")
for match in pattern.finditer(html):
    # Check if there's already a comma before the newline
    end_pos = match.start() + len(match.group(0))
    quote_pos = html.find("'", match.start())
    # The quote is at position: match.start() + len("'") + len(group1) 
    quote_end = match.start() + 1 + len(match.group(1)) + 1  # position after closing quote
    # Check char after quote
    if quote_end < len(html) and html[quote_end] == ',':
        continue  # already has comma
    count += 1

print(f"Missing commas found: {count}")

# Now fix them
def add_comma(match):
    value = match.group(1)
    next_key = match.group(2)
    return f"'{value}',\n{next_key}"

fixed = pattern.sub(add_comma, html)
# But this would double-comma. Let me be more careful.

# Actually, let me use a different approach: only match where char after closing quote is NOT a comma
# The pattern 'value'\n where the char before \n is ' (not ',)
# So match 'value' where followed by \n (not ,\n)
fixed = re.sub(r"(?<=')\n(?=\s+[a-z_][a-z_0-9]*:)", ",", html)

print(f"After: {len(fixed)} bytes (+{len(fixed)-len(html)} commas)")

with open('D:/tokai/index-fixed3.html', 'w', encoding='utf-8') as f:
    f.write(fixed)

# Validate
start = fixed.find('<script>')
end = fixed.rfind('</script>')
js = fixed[start+8:end]
with open('D:/tokai/check3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print(f"JS: {len(js)} chars, braces: {js.count('{')}:{js.count('}')}")
