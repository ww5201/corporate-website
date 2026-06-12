import paramiko, re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Server size: {len(html)}")
print(f"settings-menu count: {html.count('settings-menu')}")

# Remove ALL settings divs
html = re.sub(r'<div class="settings-[^"]*"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
print(f"After cleanup: {len(html)}")

# Insert ☰ button before lang-switch
html = re.sub(r'(<div class="lang-switch">)', r'<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>\n      \1', html)
print(f"After insert: {len(html)}")

# Add dropdown
dropdown = '\n      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:80px;top:60px;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden"><a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0"><span>🔄</span> 版本更新</a><a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem"><span>🗑️</span> 清除缓存</a></div>\n'
if 'settingsDropdown' not in html:
    html = html.replace('</nav>', dropdown + '    </nav>')
    print("Added dropdown")

# Validate
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Save and upload
with open(r'D:/tokai/index-fixed.html', 'w', encoding='utf-8') as f:
    f.write(html)

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('OK');}catch(err){console.log('ERR:'+err.message);}\"")
js_val = stdout.read().decode().strip()

ssh.close()

print(f"\nDone! Size: {size}, JS: {js_val}")
