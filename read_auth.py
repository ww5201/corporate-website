import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# Read current auth.js
stdin, stdout, stderr = ssh.exec_command('cat /root/backend/routes/auth.js')
auth_content = stdout.read().decode('utf-8', errors='replace')
print("=== CURRENT AUTH.JS ===")
print(auth_content[:5000])

ssh.close()
