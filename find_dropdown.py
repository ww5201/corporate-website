import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command("grep -n 'settingsDropdown' /var/www/frontend/index.html")
lines = stdout.read().decode('utf-8')

print("settingsDropdown occurrences:")
print(lines)

ssh.close()
