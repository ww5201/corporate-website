import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/')
http = stdout.read().decode().strip()
print(f"HTTP status: {http}")

stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/health')
api = stdout.read().decode().strip()
print(f"API health: {api}")

stdin, stdout, stderr = ssh.exec_command('systemctl is-active nginx')
nginx = stdout.read().decode().strip()
print(f"Nginx: {nginx}")

ssh.close()
