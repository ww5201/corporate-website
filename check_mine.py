import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()

# Read mine.html (profile page)
f = sftp.file('/var/www/frontend/mine.html', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Find sections related to menu/profile items
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'menu' in line.lower() or 'about' in line.lower() or 'logout' in line.lower() or 'exit' in line.lower() or 'setting' in line.lower() or 'mine' in line.lower():
        start = max(0, i-1)
        end = min(len(lines), i+3)
        for j in range(start, end):
            safe = lines[j].encode('ascii', 'replace').decode('ascii')
            print(f'{j+1}: {safe}')
        print()

sftp.close()
ssh.close()
