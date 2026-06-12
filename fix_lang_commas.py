import re

with open('D:/tokai/index-fixed4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract JS
start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]

# Fix 1: Add commas between language sections
# Pattern: }\n      en: {  (or ja:, ko:, etc.)
# These should be },\n      en: {
# Match: } followed by newline+spaces+lang_code: {
js_fixed = re.sub(r'\}\s*\n(\s+)([a-z]{2}: \{)', r'},\n\1\2', js)

# Fix 2: Remove multiple consecutive commas (from zh section)
js_fixed = re.sub(r',+', ',', js_fixed)

# Fix 3: Ensure semicolon at end of i18n = {...};
# Pattern: }\n  };  should be correct
# But };  needs to be },  before the final };

# Count changes
print(f"JS before: {len(js)}, after: {len(js_fixed)}")

# Reconstruct HTML
fixed_html = html[:start+8] + js_fixed + html[end:]

with open('D:/tokai/index-fixed5.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

with open('D:/tokai/check5.js', 'w', encoding='utf-8') as f:
    f.write(js_fixed)

print(f"Saved: {len(fixed_html)} bytes, braces: {js_fixed.count('{')}:{js_fixed.count('}')}")
