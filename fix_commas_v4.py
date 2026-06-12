import re

# Read the original fixed file
with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Original: {len(html)} bytes")

# Extract JS
script_start = html.find('<script>')
script_end = html.rfind('</script>')
js = html[script_start+8:script_end]

# Strategy: find the i18n object by looking for "const i18n = {" pattern
# and fix ALL missing commas in it (between any key-value pairs)
# 
# The i18n object has structure:
# const i18n = {
#   zh: {
#     key1: 'value1',
#     key2: 'value2'    <-- missing comma here
#     key3: 'value3',
#   },
#   en: { ... },
#   ...
# };
#
# We need to add commas where a line ending with 'value' or "value"
# is followed by a line starting with spaces + identifier:

# Pattern: line ending with 'value' (no comma) followed by line with key:
# This means: ' then newline, then spaces, then word chars, then :
# But NOT: ', then newline (already has comma)

# Let's work on the entire JS section
# Find all places where we need commas
# A missing comma looks like: 'value'\n        key:
# An existing comma looks like: 'value',\n        key:

# Count missing commas
missing = 0
fixed_js = js
# Use regex to find 'value'\n  key: patterns (where value is single-quoted)
# The key insight: if we find '\n' preceded by "'" and followed by whitespace+identifier,
# we need to check if there's already a comma

# Let's do it line by line
lines = fixed_js.split('\n')
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)

# Actually, let's use a different approach: 
# Process the entire JS and add commas after closing quotes 
# when followed by a new key on the next line

# Simple state machine approach
result = []
i = 0
fixes = 0
while i < len(js):
    result.append(js[i])
    # Check if current char is ' or " followed by \n
    if js[i] in ("'", '"') and i+1 < len(js) and js[i+1] == '\n':
        # Look ahead: skip whitespace, check if next non-ws is an identifier
        j = i + 2
        while j < len(js) and js[j] in ' \t':
            j += 1
        if j < len(js) and (js[j].isalpha() or js[j] == '_'):
            # Check if this looks like key: 
            k = j
            while k < len(js) and (js[k].isalnum() or js[k] == '_'):
                k += 1
            if k < len(js) and js[k] == ':':
                # This is a key: pattern - need comma before newline
                # Insert comma after the quote
                result.append(',')
                fixes += 1
    i += 1

fixed_js_str = ''.join(result)
print(f"Fixed {fixes} missing commas")
print(f"JS before: {len(js)}, after: {len(fixed_js_str)}")

# Reconstruct HTML
fixed_html = html[:script_start+8] + fixed_js_str + html[script_end:]
print(f"HTML: {len(html)} -> {len(fixed_html)} bytes")

# Save
with open('D:/tokai/index-fixed3.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

# Write JS for validation
with open('D:/tokai/check3.js', 'w', encoding='utf-8') as f:
    f.write(fixed_js_str)

print("Saved index-fixed3.html")
