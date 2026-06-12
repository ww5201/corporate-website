import re

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Start: {len(html)} bytes")

# ===== STEP 1: Fix i18n object commas =====
# Extract JS
script_start = html.find('<script>')
script_end = html.rfind('</script>')
js = html[script_start+8:script_end]

# Find i18n object
i18n_match = re.search(r'const i18n\s*=\s*\{', js)
i18n_start = i18n_match.start()
depth = 0
i18n_end = i18n_match.end() - 1
for i in range(i18n_match.end() - 1, len(js)):
    if js[i] == '{': depth += 1
    elif js[i] == '}': depth -= 1
    if depth == 0:
        i18n_end = i + 1
        break

i18n = js[i18n_start:i18n_end]
print(f"i18n: {len(i18n)} chars")

# Aggressive fix: add comma after every ' or " that is:
# 1. Inside the i18n object
# 2. Followed by newline
# 3. NOT already followed by comma
# 4. The next non-blank line starts with an identifier or }

# First, remove any multiple commas
i18n = re.sub(r',+', ',', i18n)

# Now add missing commas
lines = i18n.split('\n')
fixed_lines = []
fix_count = 0

for i, line in enumerate(lines):
    stripped = line.rstrip()
    
    # Check if line ends with ' or " (possibly with trailing spaces)
    # but NOT with ', or ",
    if stripped and stripped[-1] in ("'", '"'):
        if len(stripped) >= 2 and stripped[-2] == ',':
            # Already has comma
            fixed_lines.append(line)
            continue
        
        # Check next non-empty line
        next_line = ''
        for j in range(i+1, len(lines)):
            if lines[j].strip():
                next_line = lines[j].strip()
                break
        
        # Add comma if next line is a key: or } or lang: {
        should_add = False
        if next_line:
            if re.match(r'^[a-z_][a-z_0-9]*\s*:', next_line):
                should_add = True
            elif next_line.startswith('}'):
                should_add = True
            elif re.match(r'^[a-z]{2}:\s*\{', next_line):
                should_add = True
        
        if should_add:
            stripped = stripped + ','
            fix_count += 1
    
    # Also fix lines ending with } that need comma before next lang block
    elif stripped and stripped.rstrip()[-1] == '}':
        check = stripped.rstrip()
        if not check.endswith('},') and not check.endswith('};'):
            next_line = ''
            for j in range(i+1, len(lines)):
                if lines[j].strip():
                    next_line = lines[j].strip()
                    break
            if next_line and re.match(r'^[a-z]{2}:\s*\{', next_line):
                stripped = stripped.rstrip() + ','
                fix_count += 1
    
    fixed_lines.append(stripped)

fixed_i18n = '\n'.join(fixed_lines)
print(f"Fixed {fix_count} commas in i18n")

# ===== STEP 2: Fix other issues =====

# Remove old toggleLangMenu function
# (skip - already handled)

# Fix async function separation (remove blank lines between async and function)
# (already handled in previous script)

# Add missing functions
if 'function showContact()' not in js:
    js_new = js[:i18n_start] + fixed_i18n + js[i18n_end:]
    js_new = js_new.replace(
        'function closeOrder()',
        'function showContact() { document.getElementById("contact").scrollIntoView({behavior:"smooth"}); }\n    function closeOrder()'
    )
    print("Added showContact")
else:
    js_new = js[:i18n_start] + fixed_i18n + js[i18n_end:]

# Add toggleMenu if missing
if 'function toggleMenu()' not in js_new:
    js_new = js_new.replace(
        'function setLang(',
        'function toggleMenu() { var m = document.getElementById("menu"); if(m) m.classList.toggle("show"); }\n    function setLang('
    )
    print("Added toggleMenu")

# ===== STEP 3: Reconstruct HTML =====
html_new = html[:script_start+8] + js_new + html[script_end:]

# Add .menu.show CSS if missing
if '.menu.show' not in html_new:
    html_new = html_new.replace(
        '.menu { display: none; }',
        '.menu { display: none; }\n        .menu.show { display: block; position: absolute; top: 100%; left: 0; right: 0; background: var(--bg); padding: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }'
    )
    print("Added .menu.show CSS")

# ===== SAVE =====
with open('D:/tokai/index-fixed-final.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print(f"\nFinal: {len(html_new)} bytes")

# Extract JS for validation
start = html_new.find('<script>')
end = html_new.rfind('</script>')
js_final = html_new[start+8:end]
with open('D:/tokai/check-final.js', 'w', encoding='utf-8') as f:
    f.write(js_final)
print(f"JS: {len(js_final)} chars, braces: {js_final.count('{')}:{js_final.count('}')}")
