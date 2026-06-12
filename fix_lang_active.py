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

# Fix setLang: add button active state update
old_setlang_line = """      // langDropdown removed - using settings dropdown instead

      document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';"""

new_setlang_line = """      // Update active state on language buttons in settings dropdown
      document.querySelectorAll('#settingsDropdown button[onclick^=\"setLang\"]').forEach(btn => {
        const btnLang = btn.getAttribute('onclick').match(/setLang\\('([a-z]+)'\\)/);
        if (btnLang && btnLang[1] === lang) {
          btn.style.background = '#f5f5f5';
          btn.style.borderColor = '#007bff';
        } else {
          btn.style.background = 'none';
          btn.style.borderColor = '#e0e0e0';
        }
      });

      document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';"""

if old_setlang_line in js:
    js = js.replace(old_setlang_line, new_setlang_line)
    print("FIX: Added button active state update")
else:
    print("Pattern not found, checking actual content...")
    idx = js.find('// langDropdown removed')
    if idx >= 0:
        print(f"Found at {idx}: ...{js[idx:idx+100]}...")

# Rebuild and upload
new_html = html[:js_start] + js + html[js_end:]

sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(new_html)
f.close()
sftp.close()

# Save local
with open('D:/tokai/server_lang_fixed.html', 'w', encoding='utf-8') as out:
    out.write(new_html)

# Verify
final_js = new_html[new_html.find('<script>')+8:new_html.rfind('</script>')]
print(f"File: {len(new_html)} bytes, JS braces: {final_js.count('{')}:{final_js.count('}')}")
print("Uploaded!")

ssh.close()
