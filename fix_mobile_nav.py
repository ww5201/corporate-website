import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find mobile nav
m = html.find('<nav class="mobile-nav">')
me = html.find('</nav>', m) + 6
mobile = html[m:me]

# Write to file for inspection
with open('D:/tokai/mobile_nav.txt', 'w', encoding='utf-8') as f:
    f.write(mobile)

# Check if settings is there
has_settings = '\u2699' in mobile
print(f"Has settings: {has_settings}")
print(f"Mobile nav length: {len(mobile)}")

# Find inner div
inner_start = mobile.find('<div class="mobile-nav-inner">')
if inner_start >= 0:
    inner_end = mobile.find('</div>', inner_start) + 6
    inner = mobile[inner_start:inner_end]
    print(f"Inner length: {len(inner)}")
    
    # Add settings link before closing div
    settings_link = '      <a href="javascript:void(0)" onclick="toggleSettings()" style="color:#555"><span class="icon">\u2699</span>\u8bbe\u7f6e</a>\n'
    if settings_link not in inner:
        new_inner = inner.replace('</div>', settings_link + '    </div>', 1)
        new_mobile = mobile[:inner_start] + new_inner + mobile[inner_end:]
        html = html[:m] + new_mobile + html[me:]
        print("Added settings to mobile nav")
    else:
        print("Settings already in mobile nav")
else:
    print("No inner div found")

# Validate
js = html[html.find('<script>')+8:html.rfind('</script>')]
print(f"JS balanced: {js.count('{')==js.count('}')}")

# Save
with open('D:/tokai/index-final-settings.html', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(html)

# Upload
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode('utf-8').strip()
print(f"Server size: {size}")

ssh.close()
