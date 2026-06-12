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

# ============================================================
# FIX 1: setLang function - remove #langDropdown references
# ============================================================
old_setLang_block = """      document.querySelectorAll('#langDropdown button').forEach(b => b.classList.toggle('active', b.textContent.includes(langLabels[lang])));

      document.getElementById('langDropdown').classList.remove('open');"""

new_setLang_block = """      // langDropdown removed - using settings dropdown instead"""

if old_setLang_block in js:
    js = js.replace(old_setLang_block, new_setLang_block)
    print("FIX 1: Removed #langDropdown references from setLang")
else:
    print("WARNING: FIX 1 pattern not found!")
    # Try to find what's actually there
    idx = js.find('#langDropdown')
    if idx >= 0:
        print(f"  Found #langDropdown at offset {idx}: ...{js[max(0,idx-30):idx+50]}...")

# ============================================================
# FIX 2: toggleSettings - add stopPropagation + close on outside click
# ============================================================
old_toggle = """function toggleSettings() {
      var dd = document.getElementById('settingsDropdown');
      dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    }"""

new_toggle = """function toggleSettings(e) {
      if(e) e.stopPropagation();
      var dd = document.getElementById('settingsDropdown');
      if(dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    }
    // Close settings when clicking outside
    document.addEventListener('click', function(ev) {
      var dd = document.getElementById('settingsDropdown');
      if(dd && !ev.target.closest('.settings-dropdown') && !ev.target.closest('[onclick*=\"toggleSettings\"]')) {
        dd.style.display = 'none';
      }
    });"""

if old_toggle in js:
    js = js.replace(old_toggle, new_toggle)
    print("FIX 2: Updated toggleSettings with stopPropagation + click-outside close")
else:
    # Check what's actually there
    idx = js.find('function toggleSettings')
    if idx >= 0:
        actual = js[idx:idx+200]
        print(f"  Actual toggleSettings: {actual[:150]}")

# ============================================================
# FIX 3: Check for any other missing element references
# ============================================================
issues = []
dangerous_patterns = [
    ('getElementById(\'langDropdown\')', 'langDropdown ID'),
    ('querySelectorAll(\'#langDropdown', 'langDropdown selector'),
    ('currentLangLabel', 'currentLangLabel'),
    ('.settings-menu', 'settings-menu class'),
]

for pattern, name in dangerous_patterns:
    count = js.count(pattern)
    if count > 0:
        issues.append(f"  STILL HAS {count}x '{pattern}' ({name})")

if issues:
    print("\nREMAINING ISSUES:")
    for issue in issues:
        print(issue)
else:
    print("\nNo remaining issues found!")

# ============================================================
# Rebuild HTML with fixed JS
# ============================================================
new_html = html[:js_start] + js + html[js_end:]

# Final validation
final_js = new_html[new_html.find('<script>')+8:new_html.rfind('</script>')]
braces_open = final_js.count('{')
braces_close = final_js.count('}')
print(f"\nFinal file: {len(new_html)} bytes")
print(f"JS braces: {braces_open}:{braces_close} {'BALANCED' if braces_open==braces_close else 'UNBALANCED!'}")

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(new_html)
f.close()
sftp.close()

# Save local copy
with open('D:/tokai/server_fixed.html', 'w', encoding='utf-8') as out:
    out.write(new_html)

print("Uploaded successfully!")

ssh.close()
