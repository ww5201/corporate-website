import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\dist\index.html', '/root/backend/frontend/index.html')
print('OK: index.html uploaded to /root/backend/frontend/index.html')
# Also check if the old assets exist on remote
stdin, stdout, stderr = ssh.exec_command('ls -la /root/backend/frontend/assets/ 2>&1', timeout=10)
print(stdout.read().decode('utf-8', 'replace'))
sftp.close()
ssh.close()
