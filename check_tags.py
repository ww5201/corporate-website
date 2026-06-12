import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Check what we have
for tag in ['<body', '</body>', '</html>', '<script>', '</script>']:
    c = html.count(tag)
    print(f"{tag}: {c}")

# Show last 500 chars
print("\nLast 500 chars:")
print(repr(html[-500:]))

# Show around position 75000 (where second head starts)
print("\nAround 74990-75020:")
print(repr(html[74990:75020]))

ssh.close()
