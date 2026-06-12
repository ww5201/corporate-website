import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download fresh from server
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Before: {len(html)}")

# Remove duplicate button
btn = '<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="\u8bbe\u7f6e">\u2630</button>'
count = html.count(btn)
print(f"Button count: {count}")
if count > 1:
    idx = html.find(btn)
    html = html[:idx] + html[idx+len(btn):]
    print("Removed one button")

# Remove lang-switch div
ls_start = html.find('<div class="lang-switch">')
if ls_start >= 0:
    depth = 0
    for i in range(ls_start, len(html)):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                html = html[:ls_start] + html[i+6:]
                print("Removed lang-switch")
                break

# Remove settings-dropdown divs
while True:
    dd = html.find('<div class="settings-dropdown"')
    if dd < 0:
        break
    depth = 0
    for i in range(dd, len(html)):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                html = html[:dd] + html[i+6:]
                print("Removed settings-dropdown")
                break

# Add new settings button + dropdown before first </nav>
nav_end = html.find('</nav>')
if nav_end >= 0:
    settings = '\n      <div style="position:relative;margin-left:8px">\n'
    settings += '        <button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:6px 10px;border-radius:8px;color:#555" title="\u8bbe\u7f6e">\u2699</button>\n'
    settings += '        <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:200px;z-index:9999;overflow:hidden">\n'
    settings += '          <div style="padding:12px 16px;border-bottom:1px solid #f0f0f0">\n'
    settings += '            <div style="font-size:0.75rem;color:#999;margin-bottom:8px">\u8bed\u8a00 / Language</div>\n'
    settings += '            <div style="display:flex;flex-wrap:wrap;gap:4px">\n'
    langs = [
        ('zh', '\U0001f1e8\U0001f1f3 \u4e2d\u6587'),
        ('en', '\U0001f1fa\U0001f1f8 EN'),
        ('ja', '\U0001f1ef\U0001f1f5 \u65e5\u672c\u8a9e'),
        ('ko', '\U0001f1f0\U0001f1f7 \ud55c\uad6d\uc5b4'),
        ('th', '\U0001f1f9\U0001f1ed \u0e44\u0e17\u0e22'),
        ('vi', '\U0001f1fb\U0001f1f3 Ti\u1ebfng Vi\u1ec7t'),
        ('ms', '\U0001f1f2\U0001f1fe Melayu'),
    ]
    for code, label in langs:
        settings += f'              <button onclick="setLang(\'{code}\')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">{label}</button>\n'
    settings += '            </div>\n'
    settings += '          </div>\n'
    settings += '          <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background=\'#f8f8f8\'" onmouseout="this.style.background=\'transparent\'"><span>\U0001f504</span> \u7248\u672c\u66f4\u65b0</a>\n'
    settings += '          <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background=\'#f8f8f8\'" onmouseout="this.style.background=\'transparent\'"><span>\U0001f5d1\ufe0f</span> \u6e05\u9664\u7f13\u5b58</a>\n'
    settings += '        </div>\n'
    settings += '      </div>\n'
    html = html[:nav_end] + settings + '    ' + html[nav_end:]
    print("Added settings with gear icon + languages + update + cache")

# Fix toggleSettings
old_ts = 'function toggleSettings() {\n      var dd = document.getElementById(\'settingsDropdown\');\n      if (dd) dd.style.display = dd.style.display === \'none\' ? \'block\' : \'none\';\n    }'
new_ts = 'function toggleSettings(e) {\n      if (e) e.stopPropagation();\n      var dd = document.getElementById(\'settingsDropdown\');\n      if (dd) dd.style.display = dd.style.display === \'none\' ? \'block\' : \'none\';\n    }\n    document.addEventListener(\'click\', function(e) {\n      var dd = document.getElementById(\'settingsDropdown\');\n      if (dd && !e.target.closest(\'.settings-dropdown\') && !e.target.closest(\'[onclick*="toggleSettings"]\')) {\n        dd.style.display = \'none\';\n      }\n    });'
if old_ts in html:
    html = html.replace(old_ts, new_ts)
    print("Fixed toggleSettings")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Save locally
with open(r'D:/tokai/index-settings.html', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(html)

# Upload
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode('utf-8').strip()

stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK');}catch(err){console.log('ERR:'+err.message);}\"")
js_val = stdout.read().decode('utf-8').strip()

ssh.close()

print(f"\nServer: {size}, JS: {js_val}")
