import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Before: {len(html)}")

# Remove duplicate ☰ button (keep only first one)
button_html = '<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>'
count = html.count(button_html)
print(f"Button count: {count}")

if count > 1:
    # Remove all but first
    first_idx = html.find(button_html)
    # Replace second occurrence with empty
    second_idx = html.find(button_html, first_idx + 10)
    if second_idx > first_idx:
        html = html[:second_idx] + html[second_idx + len(button_html):]
        # Also remove the newline after it if present
        if html[second_idx:second_idx+10].strip() == '':
            html = html[:second_idx] + html[second_idx:].lstrip('\n')
    print(f"After removing duplicate button: {len(html)}")

# Remove duplicate dropdown from mobile nav
# The desktop nav ends with </nav> and mobile nav also has </nav>
# We only want dropdown in desktop nav
dropdown = '''
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:80px;top:60px;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem"><span>🗑️</span> 清除缓存</a>
      </div>
'''

dropdown_count = html.count(dropdown)
print(f"Dropdown count: {dropdown_count}")

if dropdown_count > 1:
    # Remove second occurrence
    first_idx = html.find(dropdown)
    second_idx = html.find(dropdown, first_idx + 10)
    if second_idx > first_idx:
        html = html[:second_idx] + html[second_idx + len(dropdown):]
    print(f"After removing duplicate dropdown: {len(html)}")

# Validate
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Save locally
with open(r'D:/tokai/index-clean-final.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Upload
sftp.close()
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

print(f"\nServer size: {size}")
print(f"JS: {js_val}")
print(f"Local: D:/tokai/index-clean-final.html ({len(html)} bytes)")
