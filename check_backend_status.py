import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查后端状态
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000 | head -5")
port3000 = stdout.read().decode('utf-8').strip()

# 检查所有node进程
stdin, stdout, stderr = ssh.exec_command("ps aux | grep 'node\\|next' | grep -v grep")
processes = stdout.read().decode('utf-8', errors='replace').strip()

# 检查后端健康
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8').strip()

# 检查数据库文件
stdin, stdout, stderr = ssh.exec_command("ls -la /root/backend/data/")
dbs = stdout.read().decode('utf-8').strip()

# 检查server-v4.js是否存在
stdin, stdout, stderr = ssh.exec_command("ls -la /root/backend/server-v4.js")
sv4 = stdout.read().decode('utf-8').strip()

with open(r'D:\tokai\backend_status.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Port 3000 ===\n{port3000}\n\n")
    f.write(f"=== Processes ===\n{processes}\n\n")
    f.write(f"=== Health ===\n{health}\n\n")
    f.write(f"=== DBs ===\n{dbs}\n\n")
    f.write(f"=== server-v4.js ===\n{sv4}")

ssh.close()
print("Done")
