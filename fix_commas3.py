import urllib.request
import re

url = 'http://8.138.218.146/'
response = urllib.request.urlopen(url, timeout=30)
html = response.read().decode('utf-8')

print("Downloaded: %d bytes" % len(html))

script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if not script_match:
    print("NO SCRIPT!")
    exit(1)

js = script_match.group(1)

# Find i18n section
i18n_start = js.find('const i18n = {')
i18n_end = js.find('    // =====', i18n_start)  # Next section marker
if i18n_end < 0:
    i18n_end = js.find('    window.addEventListener', i18n_start)

i18n_section = js[i18n_start:i18n_end]

# Simple fix: replace patterns like "nav_contact: '联系'\n        hero_badge" with "nav_contact: '联系',\n        hero_badge"
# Match: word: 'anything' followed by newline and spaces and another word:
fixed_i18n = re.sub(r"(:\s*'[^']+')(\n\s+[a-z_]+:)", r"\1,\2", i18n_section)
fixed_i18n = re.sub(r'(:\s*"[^"]+")(\n\s+[a-z_]+:)', r'\1,\2', fixed_i18n)

fixed_js = js[:i18n_start] + fixed_i18n + js[i18n_end:]
fixed_html = html.replace(js, fixed_js, 1)

# Verify
idx = fixed_js.find('hero_badge')
if idx >= 0:
    before = fixed_js[idx-30:idx]
    print("Context: %s" % repr(before))
    if ",\n" in before:
        print("COMMA ADDED!")
    else:
        print("STILL MISSING!")

with open('D:/tokai/index-fixed2.html', 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print("Saved: %d bytes" % len(fixed_html))
