import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 停止并删除所有PM2进程
print("Stopping all PM2 processes...")
stdin, stdout, stderr = ssh.exec_command("pm2 stop all && pm2 delete all && echo done")
pm2_clean = stdout.read().decode('utf-8', errors='replace').strip()
print(f"PM2: done")

# 确认PM2状态
stdin, stdout, stderr = ssh.exec_command("pm2 list 2>&1 | cat")
pm2_list = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nPM2 list:\n{pm2_list}")

import time
time.sleep(2)

# 2. 检查端口是否释放
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000 -i :3001 2>&1 | cat")
ports = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nPorts after PM2 cleanup: {ports if ports else 'ALL FREE'}")

# 3. 启动我们的后端
print("\nStarting server-v4.js...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 & echo $!"
)
pid = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Backend PID: {pid}")

time.sleep(3)

# 4. 验证健康
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nHealth: {health}")

# 5. 验证产品API
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/products | head -c 100")
products = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Products: {products}")

# 6. 检查前端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1/ | head -3")
front = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nFrontend: {front[:150]}")

# 7. 最终进程列表
stdin, stdout, stderr = ssh.exec_command("ps aux | grep node | grep -v grep | cat")
procs = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nFinal processes:\n{procs}")

# 8. 检查PM2是否干净
stdin, stdout, stderr = ssh.exec_command("pm2 list 2>&1 | cat")
pm2_final = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nFinal PM2:\n{pm2_final}")

ssh.close()
print("\nAll done!")
