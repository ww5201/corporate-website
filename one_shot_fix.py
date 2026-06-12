import paramiko, re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download current server file
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Server size: {len(html)}")

# Count settings-menu occurrences
count = html.count('settings-menu')
print(f"settings-menu count: {count}")

# Find and show the nav section
nav_start = html.find('<nav')
nav_end = html.find('</nav>') + 6
nav = html[nav_start:nav_end]
print(f"\n=== CURRENT NAV ===")
print(nav[:1500])

# Use regex to remove ALL settings related divs
# Remove any div with class containing "settings"
html = re.sub(r'<div class="settings-[^"]*"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<button[^>]*onclick="toggleSettings[^>]*>.*?</button>', '', html, flags=re.DOTALL)

print(f"\nAfter cleanup: {len(html)}")

# Now find the correct place to insert
# Look for: </ul>\n      \n    <div class="lang-switch">
insert_pattern = r'(</ul>\s*\n\s*)\n\s*(<div class="lang-switch">)'
insert_replacement = r'\1      <button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>\n      \2'

html_new = re.sub(insert_pattern, insert_replacement, html)
print(f"After insert: {len(html_new)}")

if html_new == html:
    print("WARNING: Pattern not matched, trying alternate...")
    # Try simpler pattern
    alt_pattern = r'(<div class="lang-switch">)'
    alt_replacement = '<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>\n      \1'
    html_new = re.sub(alt_pattern, alt_replacement, html)
    print(f"After alt insert: {len(html_new)}")

# Add dropdown before </nav>
dropdown = '''
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:80px;top:60px;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
      </div>
'''

if 'settingsDropdown' not in html_new:
    html_new = html_new.replace('</nav>', dropdown + '\n    </nav>')
    print("Added dropdown")

# Validate JS
js_start = html_new.find('<script>') + 8
js_end = html_new.rfind('</script>')
js = html_new[js_start:js_end]
print(f"\nJS braces: {js.count('{')}:{js.count('}')}")

# Save locally
with open(r'D:/tokai/index-fixed.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

# Upload via SFTP
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html_new)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command('''node -e "const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK,len='+j.length);}catch(err){console.log('JS:ERR:'+err.message);}"''')
js_val = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html | head -35")
nav_final = stdout.read().decode()

ssh.close()

print(f"\n=== FINAL ===")
print(f"Remote size: {size}")
print(f"JS: {js_val}")
print(f"\n=== FINAL NAV ===\n{nav_final}")
