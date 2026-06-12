import paramiko, base64, re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download full HTML
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Original size: {len(html)}")

# === Remove ALL settings-menu related content using regex ===
# Pattern 1: The big settings-menu div block
pattern1 = r'<div class="settings-menu"[^>]*>.*?</div>\s*\n\s*'
html = re.sub(pattern1, '', html, flags=re.DOTALL)
print(f"After pattern1: {len(html)}")

# Pattern 2: Any remaining settings-menu or settings-dropdown divs
pattern2 = r'<div class="settings-[^"]*"[^>]*>.*?</div>'
html = re.sub(pattern2, '', html, flags=re.DOTALL)
print(f"After pattern2: {len(html)}")

# Pattern 3: Any standalone ☰ button with toggleSettings onclick
pattern3 = r'<button[^>]*onclick="toggleSettings\(\)"[^>]*>☰</button>\s*\n?'
html = re.sub(pattern3, '', html)
print(f"After pattern3: {len(html)}")

# Now add clean version in the right place
# Find: </ul>\n      \n    <div class="lang-switch">
# Replace with: </ul>\n      <button ...>☰</button>\n      <div class="lang-switch">

old_nav = """</ul>

      
    <div class="lang-switch">"""

new_nav = """</ul>

      <button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>
      <div class="lang-switch">"""

if old_nav in html:
    html = html.replace(old_nav, new_nav)
    print("Added clean ☰ button")
else:
    print("WARNING: nav pattern not found")

# Add dropdown menu before </nav>
dropdown = '''
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:80px;top:60px;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
      </div>
'''

if '</nav>' in html and 'settingsDropdown' not in html:
    html = html.replace('</nav>', dropdown + '\n    </nav>')
    print("Added dropdown")

print(f"Final size: {len(html)}")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = f"echo '{encoded}' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

# Save local
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify on server
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
remote_size = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command('''node -e "const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK');}catch(err){console.log('JS:ERR:'+err.message);}"''')
js_val = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html | head -30")
nav_preview = stdout.read().decode()

ssh.close()

with open('D:/tokai/final_nav.txt', 'w', encoding='utf-8') as f:
    f.write(f"Remote size: {remote_size}\n")
    f.write(f"JS: {js_val}\n\n")
    f.write(f"NAV:\n{nav_preview}\n")

print(f"\nDone! Remote: {remote_size}, JS: {js_val}")
print("See D:/tokai/final_nav.txt")
