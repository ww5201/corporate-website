import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 杀掉占用3000端口的next-server进程
print("Killing next-server on port 3000...")
stdin, stdout, stderr = ssh.exec_command("kill -9 3119 && echo 'killed' || echo 'failed'")
kill_result = stdout.read().decode('utf-8').strip()
print(f"Kill result: {kill_result}")

# 确认端口释放
import time
time.sleep(1)
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000")
port_check = stdout.read().decode('utf-8').strip()
print(f"Port 3000 now: {port_check if port_check else 'FREE'}")

# 2. 启动我们的后端
print("\nStarting our backend...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 & "
    "sleep 2 && curl -s http://127.0.0.1:3000/api/health"
)
start_result = stdout.read().decode('utf-8').strip()
print(f"Backend start: {start_result}")

# 3. 验证前端是否正确
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1/ | head -5")
front_check = stdout.read().decode('utf-8').strip()
print(f"\nFrontend check:\n{front_check[:200]}")

# 4. 检查index.html内容
stdin, stdout, stderr = ssh.exec_command("head -3 /var/www/frontend/index.html")
idx_content = stdout.read().decode('utf-8').strip()
print(f"\nIndex.html: {idx_content}")

ssh.close()
print("\nDone!")
