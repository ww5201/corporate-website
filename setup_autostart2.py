import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    ssh.exec_command(cmd)
    time.sleep(0.5)

# 先停掉手动启动的进程
run("pkill -f 'node server-v4.js'")
time.sleep(1)

# 启用并启动systemd服务
run("systemctl daemon-reload")
run("systemctl enable zhuoyi-backend.service")
run("systemctl start zhuoyi-backend.service")
time.sleep(3)

# 验证
stdin, stdout, stderr = ssh.exec_command("systemctl is-active zhuoyi-backend.service")
active = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Service active: {active}")

stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Health: {health}")

stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1/ | head -1")
front = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Frontend: {front[:60]}")

ssh.close()
print("Done!")
