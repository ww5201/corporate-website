import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Remove the entire old toggleLangMenu function + its click listener
old_lang_toggle = """    // ===== 语言切换 =====

    function toggleLangMenu(e) {

      e.stopPropagation();

      document.getElementById('langDropdown').classList.toggle('open');

    }

    document.addEventListener('click', () => document.getElementById('langDropdown').classList.remove('open'));"""

new_lang_toggle = """    // Old langDropdown removed - language selection now in settings dropdown"""

if old_lang_toggle in js:
    js = js.replace(old_lang_toggle, new_lang_toggle)
    print("Removed old toggleLangMenu function")
else:
    print("Pattern not found, trying alternative...")
    # Try finding and removing by line range
    lines = js.split('\n')
    new_lines = []
    skip = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if 'function toggleLangMenu' in line or ('// ===== 语言切换' in line):
            skip = True
            continue
        if skip:
            if "getElementById('langDropdown')" in line or ("document.addEventListener('click'" in line and 'langDropdown' in line):
                continue
            if stripped == '' and skip:
                skip = False
                continue
        new_lines.append(line)
    js = '\n'.join(new_lines)
    print(f"Manual removal done. Lines: {len(lines)} -> {len(new_lines)}")

# Verify no more langDropdown references (except comments)
issues = []
for pattern in ["getElementById('langDropdown')", "#langDropdown"]:
    count = js.count(pattern)
    if count > 0:
        for line in js.split('\n'):
            if pattern in line and '//' not in line.strip():
                issues.append(f"  Still has {pattern}: {line.strip()[:100]}")
if issues:
    print("\nRemaining issues:")
    for issue in issues:
        print(issue)
else:
    print("All langDropdown references cleaned!")

# Rebuild HTML
new_html = html[:js_start] + js + html[js_end:]

# Final validation
final_js = new_html[new_html.find('<script>')+8:new_html.rfind('</script>')]
print(f"\nFile: {len(new_html)} bytes, JS braces: {final_js.count('{')}:{final_js.count('}')}")

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(new_html)
f.close()
sftp.close()

with open('D:/tokai/server_fixed2.html', 'w', encoding='utf-8') as out:
    out.write(new_html)

print("Uploaded!")

ssh.close()
