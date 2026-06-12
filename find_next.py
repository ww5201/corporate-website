import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 检查systemd服务
stdin, stdout, stderr = ssh.exec_command("systemctl list-units --type=service --state=running | grep -i 'next\\|shop\\|video\\|app'")
services = stdout.read().decode('utf-8', errors='replace').strip()

# 2. 检查所有systemd服务文件
stdin, stdout, stderr = ssh.exec_command("ls /etc/systemd/system/*.service 2>/dev/null | head -20")
sysd = stdout.read().decode('utf-8', errors='replace').strip()

# 3. 检查pm2
stdin, stdout, stderr = ssh.exec_command("which pm2 && pm2 list 2>/dev/null || echo 'no pm2'")
pm2 = stdout.read().decode('utf-8', errors='replace').strip()

# 4. 检查crontab
stdin, stdout, stderr = ssh.exec_command("crontab -l 2>/dev/null || echo 'no crontab'")
cron = stdout.read().decode('utf-8', errors='replace').strip()

# 5. 查找next-server相关文件
stdin, stdout, stderr = ssh.exec_command("find /root /opt /home -name 'next.config*' -o -name 'package.json' -path '*/next*' 2>/dev/null | head -10")
next_files = stdout.read().decode('utf-8', errors='replace').strip()

# 6. 检查next-server的启动参数
stdin, stdout, stderr = ssh.exec_command("ps aux | grep next-server | grep -v grep | head -2")
next_proc = stdout.read().decode('utf-8', errors='replace').strip()

# 7. 检查next-server的父进程
stdin, stdout, stderr = ssh.exec_command("ps -eo pid,ppid,cmd | grep next | grep -v grep")
next_parents = stdout.read().decode('utf-8', errors='replace').strip()

# 8. 检查/opt目录
stdin, stdout, stderr = ssh.exec_command("ls -la /opt/ 2>/dev/null")
opt = stdout.read().decode('utf-8', errors='replace').strip()

# 9. 查找node_modules中的next
stdin, stdout, stderr = ssh.exec_command("find / -maxdepth 4 -name 'next-server' -type f 2>/dev/null | head -5")
next_bin = stdout.read().decode('utf-8', errors='replace').strip()

with open(r'D:\tokai\find_next.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Services ===\n{services}\n\n")
    f.write(f"=== Systemd files ===\n{sysd}\n\n")
    f.write(f"=== PM2 ===\n{pm2}\n\n")
    f.write(f"=== Crontab ===\n{cron}\n\n")
    f.write(f"=== Next files ===\n{next_files}\n\n")
    f.write(f"=== Next process ===\n{next_proc}\n\n")
    f.write(f"=== Next parents ===\n{next_parents}\n\n")
    f.write(f"=== /opt ===\n{opt}\n\n")
    f.write(f"=== Next binary ===\n{next_bin}")

ssh.close()
print("Done")
