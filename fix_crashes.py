import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Fix 1: settings-menu -> settings-dropdown (the click outside handler)
html = html.replace(".settings-menu'", ".settings-dropdown'")

# Fix 2: Remove currentLangLabel line that crashes because the element was removed
# Old: document.getElementById('currentLangLabel').textContent = langLabels[lang] || lang;
# The label was removed when we converted to dropdown, so this line throws a TypeError
old_label_line = "document.getElementById('currentLangLabel').textContent = langLabels[lang] || lang;"
new_label_line = "// currentLangLabel removed in dropdown version"
if old_label_line in html:
    html = html.replace(old_label_line, new_label_line)
    print("Fixed: removed currentLangLabel line")

# Fix 3: Check if there's a toggleSettings call that doesn't pass event
# Old toggleSettings function might need the click event to stopPropagation
old_ts = "function toggleSettings(e) {\n      if (e) e.stopPropagation();\n      var dd = document.getElementById('settingsDropdown');\n      if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';\n    }"
new_ts = "function toggleSettings(e) {\n      if (e) e.stopPropagation();\n      var dd = document.getElementById('settingsDropdown');\n      if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';\n    }"
if old_ts in html:
    print("toggleSettings already has stopPropagation")
else:
    # Might be the simple version
    old_simple = "function toggleSettings() {\n      var dd = document.getElementById('settingsDropdown');\n      if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';\n    }"
    if old_simple in html:
        html = html.replace(old_simple, new_ts)
        print("Fixed: updated toggleSettings with stopPropagation")

# Fix 4: Make sure the settings dropdown uses class settings-dropdown (not settings-menu)
# Already checked with .settings-menu' replacement above

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Verify
import re
js = html[html.find('<script>')+8:html.rfind('</script>')]
print(f"File: {len(html)} bytes")
print(f"JS: {len(js)} chars, braces: {js.count('{')}:{js.count('}')}")
print(f"settings-menu refs: {html.count('.settings-menu')}")
print(f"currentLangLabel refs: {html.count('currentLangLabel')}")

# Check products section
prod_idx = html.find('id="products"')
if prod_idx >= 0:
    prod_html = html[prod_idx:prod_idx+500]
    print(f"Products section: id=productsGrid present: {'id=\"productsGrid\"' in prod_html}")

ssh.close()
