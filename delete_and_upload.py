import paramiko, re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
print(f"Downloaded: {len(html)}")

# Remove settings-menu divs - use simple string replace
while 'settings-menu' in html:
    start = html.find('<div class="settings-menu"')
    if start < 0:
        break
    # Find matching </div>
    depth = 0
    end = start
    for i in range(start, len(html)):
        if html[i:i+5] == '<div ':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                end = i + 6
                break
    if end > start:
        html = html[:start] + html[end:]
        print(f"Removed settings-menu block, now {len(html)}")
    else:
        break

# Insert ☰ button
html = html.replace('<div class="lang-switch">', '<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>\n      <div class="lang-switch">')
print(f"After insert: {len(html)}")

# Add dropdown if not exists
if 'settingsDropdown' not in html:
    dropdown = '\n      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:80px;top:60px;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden"><a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0"><span>🔄</span> 版本更新</a><a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem"><span>🗑️</span> 清除缓存</a></div>\n'
    html = html.replace('</nav>', dropdown + '    </nav>')
    print("Added dropdown")

# Validate
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Save locally
with open(r'D:/tokai/index-clean.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved locally: {len(html)}")

# Delete remote and re-upload
sftp.remove('/var/www/frontend/index.html')
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html && node -e "const fs=require(\'fs\');const h=fs.readFileSync(\'/var/www/frontend/index.html\',\'utf8\');const s=h.indexOf(\'<script>\')+8;const e=h.lastIndexOf(\'</script>\');const j=h.substring(s,e);try{new Function(j);console.log(\'JS:OK\');}catch(err){console.log(\'JS:ERR:\'+err.message);}"')
result = stdout.read().decode()

ssh.close()
print(f"\nServer: {result}")
