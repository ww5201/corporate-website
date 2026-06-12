import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查端口和进程
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000 -i :80 2>&1 | cat")
ports = stdout.read().decode('utf-8', errors='replace')

# 检查后端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()

# 检查前端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1/ | head -3")
front = stdout.read().decode('utf-8', errors='replace').strip()

# 检查PM2
stdin, stdout, stderr = ssh.exec_command("pm2 list 2>&1 | cat")
pm2 = stdout.read().decode('utf-8', errors='replace')

# 检查node进程
stdin, stdout, stderr = ssh.exec_command("ps aux | grep node | grep -v grep | cat")
nodes = stdout.read().decode('utf-8', errors='replace')

with open(r'D:\tokai\final_status.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Ports ===\n{ports}\n\n")
    f.write(f"=== Health ===\n{health}\n\n")
    f.write(f"=== Frontend ===\n{front[:200]}\n\n")
    f.write(f"=== PM2 ===\n{pm2}\n\n")
    f.write(f"=== Node processes ===\n{nodes}")

ssh.close()
print("Done")
