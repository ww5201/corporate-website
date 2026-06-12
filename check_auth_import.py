import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# Check how auth.js is imported in server-v4.js around line 135
stdin, stdout, stderr = ssh.exec_command('sed -n "125,145p" /root/backend/server-v4.js')
lines = stdout.read().decode('utf-8', errors='replace')
print("[1] server-v4.js lines 125-145:")
print(lines)

# Also check the import line for auth
stdin, stdout, stderr = ssh.exec_command('grep -n "auth" /root/backend/server-v4.js | head -10')
auth_refs = stdout.read().decode('utf-8', errors='replace')
print("\n[2] Auth references:")
print(auth_refs)

ssh.close()
