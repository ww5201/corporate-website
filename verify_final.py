import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
f = sftp.file('/var/www/frontend/login.html', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

lines = content.split('\n')
for i in range(449, min(468, len(lines))):
    safe = lines[i].encode('ascii', 'replace').decode('ascii')
    print(f'{i+1}: {safe}')

sftp.close()
ssh.close()
