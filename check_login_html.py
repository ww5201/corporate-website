import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
f = sftp.file('/var/www/frontend/login.html', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

lines = content.split('\n')
for i, line in enumerate(lines):
    lower = line.lower()
    if any(kw in lower for kw in ['profile', 'mine', 'about', 'privacy', 'setting', 'logout', 'menu-item', 'user-info', 'user-menu']):
        start = max(0, i-1)
        end = min(len(lines), i+4)
        for j in range(start, end):
            safe = lines[j].encode('ascii', 'replace').decode('ascii')
            print(f'{j+1}: {safe}')
        print()

sftp.close()
ssh.close()
