import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 检查nginx状态
stdin, stdout, stderr = ssh.exec_command("systemctl status nginx 2>&1 | head -5")
nginx = stdout.read().decode('utf-8', errors='replace').strip()

# 2. 检查端口
stdin, stdout, stderr = ssh.exec_command("ss -tlnp | grep -E ':80|:3000'")
ports = stdout.read().decode('utf-8', errors='replace').strip()

# 3. 检查后端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health 2>&1")
health = stdout.read().decode('utf-8', errors='replace').strip()

# 4. 检查PM2是否又启动了
stdin, stdout, stderr = ssh.exec_command("pm2 list 2>&1 | cat")
pm2 = stdout.read().decode('utf-8', errors='replace')

# 5. 检查swap是否还在
stdin, stdout, stderr = ssh.exec_command("free -h | grep Swap")
swap = stdout.read().decode('utf-8', errors='replace').strip()

with open(r'D:\tokai\restart_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Nginx ===\n{nginx}\n\n")
    f.write(f"=== Ports ===\n{ports}\n\n")
    f.write(f"=== Health ===\n{health}\n\n")
    f.write(f"=== PM2 ===\n{pm2}\n\n")
    f.write(f"=== Swap ===\n{swap}")

ssh.close()
print("Done")
