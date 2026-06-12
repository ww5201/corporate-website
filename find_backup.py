import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check for backups on server
stdin, stdout, stderr = ssh.exec_command('ls -la /var/www/frontend/*.html* /root/frontend*.zip 2>/dev/null')
print("Backups:")
print(stdout.read().decode())

# Check current file size
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
print("\nCurrent:", stdout.read().decode().strip())

# Check if there's an original backup
stdin, stdout, stderr = ssh.exec_command('ls -la /var/www/frontend/index.html.bak 2>/dev/null; ls -la /root/frontend*.zip 2>/dev/null')
print(stdout.read().decode())

ssh.close()
