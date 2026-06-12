import paramiko
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=10)

print("=== 1. Product API ===")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/products')
p = stdout.read().decode()
print(f"Products: {p[:300]}")

print("\n=== 2. Messages/Inquiries API ===")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/messages')
m = stdout.read().decode()
print(f"Messages: {m[:300]}")

print("\n=== 3. Cases API ===")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/cases')
c = stdout.read().decode()
print(f"Cases: {c[:200]}")

print("\n=== 4. Admin page check ===")
stdin, stdout, stderr = ssh.exec_command('ls -la /root/backend/admin.html /root/backend/server-v4.js /root/backend/data/ 2>&1')
print(stdout.read().decode())

print("\n=== 5. Data files ===")
stdin, stdout, stderr = ssh.exec_command('ls -la /root/backend/data/ 2>&1')
print(stdout.read().decode())

ssh.close()
