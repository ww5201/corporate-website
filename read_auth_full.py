import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

stdin, stdout, stderr = ssh.exec_command('cat /root/backend/routes/auth.js')
content = stdout.read().decode('utf-8', errors='replace')

# Print full content length and last part
print(f"Total length: {len(content)}")
print("=== FULL FILE ===")
print(content)

ssh.close()
