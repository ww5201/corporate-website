import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 杀掉所有 next-server 进程
print("Killing next-server processes...")
stdin, stdout, stderr = ssh.exec_command("pkill -f next-server && echo 'killed' || echo 'none'")
kill1 = stdout.read().decode('utf-8').strip()
print(f"Kill next-server: {kill1}")

# 确认杀掉
import time
time.sleep(1)

# 2. 杀掉端口3000上的任何进程
stdin, stdout, stderr = ssh.exec_command("fuser -k 3000/tcp 2>/dev/null; echo 'done'")
fuser = stdout.read().decode('utf-8').strip()
print(f"Fuser: {fuser}")

time.sleep(1)

# 3. 确认端口释放
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000")
p3000 = stdout.read().decode('utf-8').strip()
print(f"Port 3000: {p3000 if p3000 else 'FREE'}")

# 4. 启动后端
print("\nStarting backend server-v4.js...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 &"
)
start = stdout.read().decode('utf-8').strip()
print(f"Start: {start}")

time.sleep(3)

# 5. 验证健康
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8').strip()
print(f"\nHealth: {health}")

# 6. 验证产品API
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/products | head -c 200")
products = stdout.read().decode('utf-8').strip()
print(f"Products: {products}")

# 7. 验证案例API
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/cases")
cases = stdout.read().decode('utf-8').strip()
print(f"Cases: {cases}")

# 8. 检查所有运行进程
stdin, stdout, stderr = ssh.exec_command("ps aux | grep 'node\\|next' | grep -v grep")
procs = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nProcesses:\n{procs}")

# 9. 检查端口状态
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000 -i :3001 -i :80")
ports = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nPorts:\n{ports}")

ssh.close()
print("\nDone!")
