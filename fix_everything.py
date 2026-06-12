import re

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Start: {len(html)} bytes")

# ==== FIX 1: Remove extra commas in zh section ====
# mobile_consult: '咨询',,,,,,,,, -> mobile_consult: '咨询',
html = re.sub(r"mobile_consult:\s*'咨询',{2,}", "mobile_consult: '咨询',", html)

# ==== FIX 2: Remove old toggleLangMenu function ====
html = re.sub(r'\n\s*function toggleLangMenu\(\)\s*\{[^}]*\}\s*', '\n', html)

# ==== FIX 3: Fix setLang - remove #langDropdown references ====
# Remove: document.querySelectorAll('#langDropdown button').forEach(b => { ... });
html = re.sub(
    r"\s*document\.querySelectorAll\('#langDropdown button'\)\.forEach\(b\s*=>\s*\{[^}]*\}\s*\);\s*",
    '', html
)
# Remove: document.getElementById('langDropdown').classList.remove('open');
html = re.sub(
    r"\s*document\.getElementById\('langDropdown'\)\.classList\.remove\('open'\);\s*",
    '', html
)

# ==== FIX 4: Fix setLang - handle currentLangLabel ====
# Replace: currentLangLabel.textContent = ... with a safe version
html = html.replace(
    "document.getElementById('currentLangLabel').textContent = langLabels[lang]",
    "var lbl = document.getElementById('currentLangLabel'); if(lbl) lbl.textContent = langLabels[lang]"
)

# ==== FIX 5: Fix toggleSettings - add stopPropagation ====
old_toggle = """function toggleSettings() {
      var dd = document.getElementById('settingsDropdown');
      if(dd) dd.classList.toggle('open');
    }"""
new_toggle = """function toggleSettings(e) {
      if(e) e.stopPropagation();
      var dd = document.getElementById('settingsDropdown');
      if(dd) dd.classList.toggle('open');
    }"""
if old_toggle in html:
    html = html.replace(old_toggle, new_toggle)
    print("Fixed toggleSettings")

# ==== FIX 6: Fix .settings-menu -> .settings-dropdown in click outside handler ====
html = html.replace(".closest('.settings-menu')", ".closest('.settings-dropdown')")

# ==== FIX 7: Add .menu.show CSS if missing ====
if '.menu.show' not in html:
    # Find mobile media query
    mobile_css = '@media (max-width: 768px)'
    if mobile_css in html:
        # Add .menu.show after .menu { display: none; }
        html = html.replace(
            '.menu { display: none; }',
            '.menu { display: none; }\n        .menu.show { display: block; position: absolute; top: 100%; left: 0; right: 0; background: var(--bg); padding: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }'
        )
        print("Added .menu.show CSS")

# ==== FIX 8: Add toggleMenu function if missing ====
if 'function toggleMenu()' not in html:
    # Add before setLang function
    html = html.replace(
        'function setLang(',
        'function toggleMenu() { var m = document.getElementById("menu"); if(m) m.classList.toggle("show"); }\n    function setLang('
    )
    print("Added toggleMenu function")

# ==== FIX 9: Add showContact function if missing ====
if 'function showContact()' not in html:
    # Add after closeOrder function
    html = html.replace(
        'function closeOrder()',
        'function showContact() { document.getElementById("contact").scrollIntoView({behavior:"smooth"}); }\n    function closeOrder()'
    )
    print("Added showContact function")

# ==== FIX 10: Add commas in i18n object ====
# Extract JS
script_start = html.find('<script>')
script_end = html.rfind('</script>')
js = html[script_start+8:script_end]

# Find i18n object
i18n_match = re.search(r'const i18n\s*=\s*\{', js)
if i18n_match:
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
    
    # Remove multiple consecutive commas
    i18n = re.sub(r',+', ',', i18n)
    
    # Add missing commas: line ending with ' or " followed by line with key:
    lines = i18n.split('\n')
    fixed_lines = []
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        
        # Check if line ends with quoted value (no comma)
        if re.search(r"""['"]\s*$""", stripped) and not stripped.endswith("',") and not stripped.endswith('",'):
            # Look ahead
            next_content = ''
            for j in range(i+1, len(lines)):
                if lines[j].strip():
                    next_content = lines[j].strip()
                    break
            
            if next_content and (
                re.match(r'^[a-z_][a-z_0-9]*\s*:', next_content) or
                next_content.startswith('}') or
                next_content.startswith('},') or
                re.match(r'^[a-z]{2}:\s*\{', next_content)
            ):
                stripped = stripped + ','
        
        # Fix } followed by language block (need comma)
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
    
    # Reconstruct
    js = js[:i18n_start] + fixed_i18n + js[i18n_end:]
    print(f"Fixed i18n: {len(i18n)} -> {len(fixed_i18n)} chars")

# ==== FIX 11: Add langDropdown click-outside handler if missing ====
# The setLang function should also close the langDropdown
# Check if this is already handled

# Reconstruct HTML
html = html[:script_start+8] + js + html[script_end:]

# ==== SAVE ====
with open('D:/tokai/index-fixed-final.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nFinal: {len(html)} bytes")

# Validate
start = html.find('<script>')
end = html.rfind('</script>')
js_final = html[start+8:end]
with open('D:/tokai/check-final.js', 'w', encoding='utf-8') as f:
    f.write(js_final)
print(f"JS: {len(js_final)} chars, braces: {js_final.count('{')}:{js_final.count('}')}")
