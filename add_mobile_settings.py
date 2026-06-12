import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find mobile nav section
mobile_nav_start = html.find('<nav class="mobile-nav">')
if mobile_nav_start >= 0:
    mobile_nav_end = html.find('</nav>', mobile_nav_start) + 6
    mobile_nav = html[mobile_nav_start:mobile_nav_end]
    print(f"Mobile nav: {len(mobile_nav)} chars")
    
    # Check if it already has settings
    has_settings = 'settings' in mobile_nav.lower() or '\u2699' in mobile_nav
    print(f"Has settings: {has_settings}")
    
    # Find the mobile-nav-inner div
    inner_start = mobile_nav.find('<div class="mobile-nav-inner">')
    if inner_start >= 0:
        inner_end = mobile_nav.find('</div>', inner_start) + 6
        inner = mobile_nav[inner_start:inner_end]
        print(f"Inner div: {len(inner)} chars")
        
        # Add settings link before closing div
        settings_link = '      <a href="javascript:void(0)" onclick="toggleSettings()" style="color:#555"><span class="icon">\u2699</span>\u8bbe\u7f6e</a>\n'
        if settings_link not in inner:
            new_inner = inner.replace('</div>', settings_link + '    </div>', 1)
            new_mobile_nav = mobile_nav[:inner_start] + new_inner + mobile_nav[inner_end:]
            html = html[:mobile_nav_start] + new_mobile_nav + html[mobile_nav_end:]
            print("Added settings to mobile nav")

# Also update JS template for mobile nav if it's dynamically generated
# Check if there's a JS template for mobile nav
if 'mobileNav.innerHTML' in html:
    print("Found mobileNav.innerHTML in JS")
    # Find and update the template
    idx = html.find('mobileNav.innerHTML')
    if idx >= 0:
        # Show context
        context = html[max(0,idx-50):idx+200]
        print(f"Context: {context[:200]}")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Save and upload
with open(r'D:/tokai/index-mobile-settings.html', 'w', encoding='utf-8', errors='surrogatepass') as f:
    f.write(html)

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
