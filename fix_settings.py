import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Check products section
idx = html.find('id="products"')
section = html[idx:idx+1000]
print(f"Products HTML length: {len(section)}")
print(f"Has prodFilters: {'prodFilters' in section}")
print(f"Has productGrid: {'productGrid' in section}")
print(f"Has <script>: {'<script>' in section[:200]}")

# Fix settings click handler
count = html.count('.settings-menu)')
print(f"'.settings-menu)' occurrences: {count}")
html = html.replace('.settings-menu)', '.settings-dropdown)')

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Verify fix
print(f"After fix - occurrences: {html.count('.settings-menu)')}")
print(f"Has .settings-dropdown): {'.settings-dropdown)' in html}")

ssh.close()
