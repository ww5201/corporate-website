import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

# Fix 1: settings-menu -> settings-dropdown
print(f"Before fix: .settings-menu count = {html.count('.settings-menu')}")
html = html.replace(".settings-menu'", ".settings-dropdown'")
print(f"After fix: .settings-menu count = {html.count('.settings-menu')}")

# Check products section - make sure the HTML is complete
# Find renderProducts and verify it uses the right ID
js = html[html.find('<script>')+8:html.rfind('</script>')]

# Check loadData calls
print(f"\nStartup calls:")
print(f"  loadData(): {'loadData()' in js[-300:]}")
print(f"  loadCases(): {'loadCases()' in js[-300:]}")
print(f"  setLang(): {'setLang(' in js[-300:]}")

# Verify API URL
api_idx = js.find('const API')
print(f"\nAPI URL: {js[api_idx:api_idx+60]}")

# Check backend is running
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/health')
print(f"\nBackend health: {stdout.read().decode()}")

stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/products')
prod = stdout.read().decode()
print(f"Products API: {len(prod)} bytes, contains: {prod[:200]}")

# Upload fixed file
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Final check
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
print(f"\nServer file: {stdout.read().decode().strip()}")

ssh.close()
