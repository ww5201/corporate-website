import re

# Read the ORIGINAL fixed file (before my comma fixes broke anything)
with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original: {len(html)} bytes")

# Extract JS
script_start = html.find('<script>')
script_end = html.rfind('</script>')
js = html[script_start+8:script_end]

# Find i18n object boundaries
i18n_match = re.search(r'const i18n\s*=\s*\{', js)
if not i18n_match:
    print("ERROR: i18n not found")
    exit(1)

i18n_start = i18n_match.start()

# Find end by counting braces
depth = 0
i18n_end = i18n_start
for i in range(i18n_match.end() - 1, len(js)):
    if js[i] == '{': depth += 1
    elif js[i] == '}': depth -= 1
    if depth == 0:
        i18n_end = i + 1
        break

i18n = js[i18n_start:i18n_end]
print(f"i18n object: {len(i18n)} chars")
print(f"i18n start: {i18n_start}, end: {i18n_end}")

# Fix the i18n object:
# 1. Remove multiple consecutive commas
i18n = re.sub(r',+', ',', i18n)

# 2. Add commas where missing
# Strategy: process line by line
lines = i18n.split('\n')
fixed_lines = []
for i, line in enumerate(lines):
    stripped = line.rstrip()
    
    # Check if this line ends with a quoted value (no comma)
    # Patterns: key: 'value' or key: "value" (possibly with HTML inside)
    if re.search(r"""['"]\s*$""", stripped) and not stripped.endswith("',") and not stripped.endswith('",'):
        # Look ahead for next non-empty line
        next_content = ''
        for j in range(i+1, len(lines)):
            if lines[j].strip():
                next_content = lines[j].strip()
                break
        
        # Add comma if next line is a key, a closing brace, or a language block
        if next_content and (
            re.match(r'^[a-z_][a-z_0-9]*\s*:', next_content) or  # key: value
            next_content.startswith('}') or  # closing brace
            next_content.startswith('},') or  # closing brace with comma
            re.match(r'^[a-z]{2}:\s*\{', next_content)  # language block: ja: {, ko: {, etc.
        ):
            stripped = stripped + ','
    
    # Also fix lines that end with } and are followed by a language block (need comma)
    if stripped.rstrip().endswith('}') and not stripped.rstrip().endswith('},'):
        next_content = ''
        for j in range(i+1, len(lines)):
            if lines[j].strip():
                next_content = lines[j].strip()
                break
        if next_content and re.match(r'^[a-z]{2}:\s*\{', next_content):
            stripped = stripped.rstrip() + ','
    
    fixed_lines.append(stripped)

fixed_i18n = '\n'.join(fixed_lines)

# 3. Remove trailing commas before } (just to be safe)
fixed_i18n = re.sub(r',(\s*})', r'\1', fixed_i18n)

# But keep commas between language blocks: }, { needs comma
# Actually, the language blocks are like: },\n  en: { which is correct

# Reconstruct
fixed_js = js[:i18n_start] + fixed_i18n + js[i18n_end:]
fixed_html = html[:script_start+8] + fixed_js + html[script_end:]

with open('D:/tokai/index-fixed-final.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

with open('D:/tokai/check-final.js', 'w', encoding='utf-8') as f:
    f.write(fixed_js)

print(f"\nSaved: {len(fixed_html)} bytes")
print(f"JS: {len(fixed_js)} chars, braces: {fixed_js.count('{')}:{fixed_js.count('}')}")
