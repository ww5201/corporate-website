import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

js = html[html.find('<script>')+8:html.rfind('</script>')]
lines = js.split('\n')

# Find productGrid references
print("productGrid references in JS:")
for i, line in enumerate(lines):
    if 'roductGrid' in line:
        print(f"  Line {i+1}: {line.strip()[:150]}")

# Find productsGrid references  
print("\nproductsGrid references in JS:")
for i, line in enumerate(lines):
    if 'roductsGrid' in line:
        print(f"  Line {i+1}: {line.strip()[:150]}")

# Find settings clicks
print("\nsettings click handler:")
for i, line in enumerate(lines):
    if 'Close settings' in line or 'settingsDropdown' in line or 'closest' in line:
        print(f"  Line {i+1}: {line.strip()[:150]}")

ssh.close()
