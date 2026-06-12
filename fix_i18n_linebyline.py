import re

with open('D:/tokai/index-fixed3.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract JS
start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]

# Process line by line
lines = js.split('\n')
fixed_lines = []
fixes = 0

for i in range(len(lines)):
    fixed_lines.append(lines[i])

# Better approach: work on the raw text
# Find all places where a line ends with ' or " (possibly followed by spaces)
# and the next line starts with spaces + identifier:
# Add comma after the quote

# Use regex on the full text
# Match: 'value'\n<spaces>identifier: (single-quoted value, no comma)
# But NOT 'value',\n (already has comma)
# Also NOT when inside a string (tricky)

# Simplest approach: just fix the known pattern
# In the i18n object, every key-value pair should end with ,
# The pattern is: key: 'value' or key: "value"
# Followed by either , or nothing (last item before })

# Let's find the i18n object and fix it
i18n_start = js.find('const i18n = {')
if i18n_start == -1:
    print("ERROR: i18n not found")
else:
    # Find the end by counting braces from the opening { of the object
    # Skip to the first { after "const i18n = "
    brace_start = js.index('{', i18n_start)
    depth = 0
    i18n_end = brace_start
    for i in range(brace_start, len(js)):
        if js[i] == '{': depth += 1
        elif js[i] == '}': depth -= 1
        if depth == 0:
            i18n_end = i + 1
            break
    
    i18n = js[i18n_start:i18n_end]
    print(f"i18n object: {len(i18n)} chars")
    
    # Now fix the i18n object
    # Strategy: every line that has key: 'value' or key: "value"
    # should end with a comma (unless it's the last item before })
    
    i18n_lines = i18n.split('\n')
    fixed_i18n_lines = []
    for i, line in enumerate(i18n_lines):
        stripped = line.rstrip()
        
        # Check if this line ends with a quoted value (no comma)
        # Pattern: ...: 'value' or ...: "value" (no trailing comma)
        if re.search(r"""['"]\s*$""", stripped) and not stripped.endswith("',") and not stripped.endswith('",'):
            # Check if next non-empty line is a key or closing brace
            next_content = ''
            for j in range(i+1, len(i18n_lines)):
                if i18n_lines[j].strip():
                    next_content = i18n_lines[j].strip()
                    break
            
            if next_content and (re.match(r'^[a-z_][a-z_0-9]*:', next_content) or next_content.startswith('}') or next_content.startswith('},')):
                # Need comma
                line = stripped + ',' + line[len(stripped):]
                fixes += 1
        
        fixed_i18n_lines.append(line)
    
    fixed_i18n = '\n'.join(fixed_i18n_lines)
    print(f"Fixed {fixes} commas in i18n")
    
    # Also fix zh section which has extra commas
    # Remove multiple consecutive commas
    fixed_i18n = re.sub(r',+', ',', fixed_i18n)
    
    # Reconstruct JS
    fixed_js = js[:i18n_start] + fixed_i18n + js[i18n_end:]
    
    # Reconstruct HTML
    fixed_html = html[:start+8] + fixed_js + html[end:]
    
    with open('D:/tokai/index-fixed4.html', 'w', encoding='utf-8') as f:
        f.write(fixed_html)
    
    with open('D:/tokai/check4.js', 'w', encoding='utf-8') as f:
        f.write(fixed_js)
    
    print(f"Saved: {len(fixed_html)} bytes")
    print(f"JS braces: {fixed_js.count('{')}:{fixed_js.count('}')}")
