import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download and check
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    remote = f.read().decode('utf-8')
sftp.close()

with open(r'D:/tokai/index-mobile-settings.html', 'r', encoding='utf-8', errors='surrogatepass') as f:
    local = f.read()

print(f"Local: {len(local)}")
print(f"Remote: {len(remote)}")
print(f"Match: {local == remote}")

# Check mobile nav
mobile_start = remote.find('<nav class="mobile-nav">')
if mobile_start >= 0:
    mobile_end = remote.find('</nav>', mobile_start) + 6
    mobile = remote[mobile_start:mobile_end]
    has_settings = '\u2699' in mobile
    print(f"Mobile nav has settings icon: {has_settings}")

# Check desktop nav
desktop_start = remote.find('<nav class="nav"')
if desktop_start >= 0:
    desktop_end = remote.find('</nav>', desktop_start) + 6
    desktop = remote[desktop_start:desktop_end]
    has_gear = '\u2699' in desktop
    print(f"Desktop nav has gear icon: {has_gear}")

# Validate JS
js_start = remote.find('<script>') + 8
js_end = remote.rfind('</script>')
js = remote[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

ssh.close()
