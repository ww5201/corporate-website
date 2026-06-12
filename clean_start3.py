import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 停止并删除所有PM2进程
stdin, stdout, stderr = ssh.exec_command("pm2 stop all && pm2 delete all")
stdout.read()
print("PM2 cleaned")

import time
time.sleep(1)

# 2. 确认PM2干净
stdin, stdout, stderr = ssh.exec_command("pm2 list 2>&1")
pm2_out = stdout.read().decode('utf-8', errors='replace')
with open(r'D:\tokai\pm2_after.txt', 'w', encoding='utf-8') as f:
    f.write(pm2_out)

# 3. 启动后端
stdin, stdout, stderr = ssh.exec_command("cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 & echo $!")
pid = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Backend PID: {pid}")
time.sleep(3)

# 4. 验证
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health && echo '' && curl -s http://127.0.0.1/ | head -3")
result = stdout.read().decode('utf-8', errors='replace')
with open(r'D:\tokai\verify_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)

# 5. 检查端口
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000 -i :3001 2>&1 | cat")
ports = stdout.read().decode('utf-8', errors='replace')
with open(r'D:\tokai\ports_after.txt', 'w', encoding='utf-8') as f:
    f.write(ports)

# 6. 禁用PM2开机自启
stdin, stdout, stderr = ssh.exec_command("pm2 unstartup 2>&1; echo done")
stdin.read()
stdout.read()
stderr.read()
print("PM2 startup disabled")

ssh.close()
print("Done!")
