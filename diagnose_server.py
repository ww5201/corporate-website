import urllib.request
r = urllib.request.urlopen('http://8.138.218.146/', timeout=10)
html = r.read().decode('utf-8')

# Extract JS
start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]

# Check for obvious syntax errors
issues = []

# 1. Check i18n for missing commas
import re
lines = js.split('\n')
for i in range(30, 240):  # i18n section
    line = lines[i] if i < len(lines) else ''
    stripped = line.rstrip()
    if stripped and stripped[-1] in ("'", '"'):
        # Check if line ends with quote but no comma
        if len(stripped) < 2 or stripped[-2] != ',':
            # Check next non-empty line
            next_content = ''
            for j in range(i+1, min(i+5, len(lines))):
                if lines[j].strip():
                    next_content = lines[j].strip()
                    break
            if re.match(r'^[a-z_][a-z_0-9]*\s*:', next_content):
                issues.append(f"Line {i+1}: Missing comma before '{next_content[:30]}'")
            elif next_content.startswith('}') or next_content.startswith('};'):
                issues.append(f"Line {i+1}: Trailing quote before {next_content[:20]}")

# 2. Check brace balance
opens = js.count('{')
closes = js.count('}')
if opens != closes:
    issues.append(f"Brace imbalance: {opens} opens vs {closes} closes")

# 3. Check for common issues
if 'function toggleMenu()' not in js:
    issues.append("Missing toggleMenu function")
if 'function showContact()' not in js:
    issues.append("Missing showContact function")

# 4. Check i18n structure
i18n_match = re.search(r'const i18n\s*=\s*\{', js)
if i18n_match:
    depth = 0
    for i, ch in enumerate(js[i18n_match.start():]):
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
        if depth == 0:
            i18n_text = js[i18n_match.start():i18n_match.start()+i+1]
            break
    
    # Check for unclosed strings in i18n
    single_quotes = i18n_text.count("'") - i18n_text.count("\\'")
    if single_quotes % 2 != 0:
        issues.append(f"Odd number of single quotes in i18n ({single_quotes})")

if issues:
    with open('D:/tokai/issues.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(issues))
    print(f"Found {len(issues)} issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("No obvious issues found")

# Show problematic lines
print("\n=== Lines around potential issues ===")
for i in [33, 34, 35, 58, 59, 87, 88, 116, 117, 145, 146, 174, 175, 203, 204, 229, 230, 231, 232]:
    if i < len(lines):
        print(f"{i+1}: {lines[i][:120]}")
