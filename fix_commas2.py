import urllib.request
import re

# Download current HTML from server
url = 'http://8.138.218.146/'
response = urllib.request.urlopen(url, timeout=30)
html = response.read().decode('utf-8')

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

# Find the closing of i18n object
i18n_end = js.find('\n    };', i18n_start)
if i18n_end < 0:
    i18n_end = js.find('};', i18n_start + 1000)

i18n_section = js[i18n_start:i18n_end]

# Fix missing commas
lines = i18n_section.split('\n')
fixed_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if re.match(r"^[a-z_]+:\s*'[^']*'\s*$", stripped) or re.match(r'^[a-z_]+:\s*"[^"]*"\s*$', stripped):
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if re.match(r'^[a-z_]+:', next_line):
                line = line.rstrip() + ','
    fixed_lines.append(line)

fixed_i18n = '\n'.join(fixed_lines)
fixed_js = js[:i18n_start] + fixed_i18n + js[i18n_end:]
fixed_html = html.replace(js, fixed_js, 1)

print("Fixed JS: %d chars" % len(fixed_js))

# Verify
idx = fixed_js.find('hero_badge')
if idx >= 0:
    before = fixed_js[idx-20:idx]
    print("Context: %s" % repr(before))

# Save
with open('D:/tokai/index-fixed-comma.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print("Saved: %d bytes" % len(fixed_html))
