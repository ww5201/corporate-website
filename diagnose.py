import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Check JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Check critical functions
checks = [
    ('loadData', 'function loadData' in js),
    ('loadCases', 'function loadCases' in js),
    ('toggleSettings', 'function toggleSettings' in js),
    ('checkAppUpdate', 'function checkAppUpdate' in js),
    ('clearCache', 'function clearCache' in js),
]

print("Functions:")
for name, exists in checks:
    print(f"  {name}: {'OK' if exists else 'MISSING'}")

# Check startup code
startup = 'loadData()' in js and 'loadCases()' in js
print(f"\nStartup code: {'OK' if startup else 'MISSING'}")

# Check products section
has_products = 'id="products"' in html
print(f"Products section: {'OK' if has_products else 'MISSING'}")

# Check settings button position
nav = html[html.find('<nav class="nav"'):html.find('</nav>')+6]
print(f"\nNav structure:")
print(nav[:500])

# Check braces
print(f"\nJS braces: {js.count('{')}:{js.count('}')}")

ssh.close()
