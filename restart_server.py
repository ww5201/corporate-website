import paramiko
import sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=10)

print("=== Killing ALL node server processes ===")
stdin, stdout, stderr = ssh.exec_command("pkill -f 'node.*server' 2>/dev/null; pkill -f 'node.*server-v4' 2>/dev/null; sleep 1")
stdout.read()

print("=== Verify killed ===")
stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'node.*server' | grep -v grep")
procs = stdout.read().decode().strip()
print(f"Remaining: {procs if procs else 'NONE (good)'}")

print("\n=== Starting fresh backend ===")
stdin, stdout, stderr = ssh.exec_command("cd /root/backend && nohup node server-v4.js > /tmp/tokai-backend.log 2>&1 & echo $!")
pid_out = stdout.read().decode().strip()
print(f"New PID: {pid_out}")

time.sleep(3)

print("\n=== Health check ===")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/health")
print(stdout.read().decode())

print("\n=== Products API ===")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/products")
p = stdout.read().decode()
print(f"Products: {p[:200]}")

print("\n=== Messages API ===")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/messages")
m = stdout.read().decode()
print(f"Messages: {m[:200]}")

print("\n=== Cases API ===")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/cases")
c = stdout.read().decode()
print(f"Cases: {c[:200]}")

print("\n=== Port check ===")
stdin, stdout, stderr = ssh.exec_command("ss -tlnp | grep 3000")
print(stdout.read().decode().strip())

ssh.close()
print("\nDone! Backend fully restarted.")
