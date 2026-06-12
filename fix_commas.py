import requests
import re

# Download current HTML from server
url = 'http://8.138.218.146/'
response = requests.get(url, timeout=30)
html = response.text

print("Downloaded: %d bytes" % len(html))

# Extract JS
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if not script_match:
    print("NO SCRIPT TAG!")
    exit(1)

js = script_match.group(1)
print("JS: %d chars" % len(js))

# Find i18n object start and end
i18n_start = js.find('const i18n = {')
if i18n_start < 0:
    print("NO i18n OBJECT!")
    exit(1)

# Find the closing of i18n object - look for '};' after a reasonable distance
i18n_end = js.find('\n    };', i18n_start)
if i18n_end < 0:
    i18n_end = js.find('};', i18n_start + 1000)

i18n_section = js[i18n_start:i18n_end]

# Fix missing commas: find lines that end with a value but no comma, followed by a line starting with a key
lines = i18n_section.split('\n')
fixed_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    # Check if this line looks like a key-value pair without trailing comma
    if re.match(r"^[a-z_]+:\s*'[^']*'\s*$", stripped) or re.match(r'^[a-z_]+:\s*"[^"]*"\s*$', stripped):
        # Check if next line starts with a key (indicating this line needs a comma)
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if re.match(r'^[a-z_]+:', next_line):
                # Add comma
                line = line.rstrip() + ','
    fixed_lines.append(line)

fixed_i18n = '\n'.join(fixed_lines)

# Replace in JS
fixed_js = js[:i18n_start] + fixed_i18n + js[i18n_end:]

# Replace in HTML
fixed_html = html.replace(js, fixed_js, 1)

print("Fixed JS: %d chars" % len(fixed_js))

# Verify syntax
try:
    # Simple check - look for the pattern that caused the error
    if 'hero_badge' in fixed_js:
        idx = fixed_js.find('hero_badge')
        before = fixed_js[idx-20:idx]
        print("Context before hero_badge: %s" % before)
        if before.strip().endswith(','):
            print("Comma check: OK")
        else:
            print("Comma check: STILL MISSING!")
except Exception as e:
    print("Check error: %s" % e)

# Save locally
with open('D:/tokai/index-fixed-comma.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print("Saved to D:/tokai/index-fixed-comma.html")
print("File size: %d bytes" % len(fixed_html))
