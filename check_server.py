import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查后端健康
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()

# 检查 nginx
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/")
nginx_code = stdout.read().decode('utf-8', errors='replace').strip()

# 检查内存
stdin, stdout, stderr = ssh.exec_command("free -m | head -3")
mem = stdout.read().decode('utf-8', errors='replace').strip()

# 检查进程
stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'node|nginx|mysql' | grep -v grep | head -10")
procs = stdout.read().decode('utf-8', errors='replace').strip()

# 检查前端文件大小
stdin, stdout, stderr = ssh.exec_command("wc -c /var/www/frontend/index.html")
fsize = stdout.read().decode('utf-8', errors='replace').strip()

# 检查 nginx 错误日志
stdin, stdout, stderr = ssh.exec_command("tail -5 /var/log/nginx/error.log 2>/dev/null || echo 'no error log'")
nerr = stdout.read().decode('utf-8', errors='replace').strip()

# 检查后端日志
stdin, stdout, stderr = ssh.exec_command("ls -la /root/backend/server-v4.js")
blog = stdout.read().decode('utf-8', errors='replace').strip()

with open(r'D:\tokai\status_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"Backend health: {health}\n")
    f.write(f"Nginx status: {nginx_code}\n")
    f.write(f"\nMemory:\n{mem}\n")
    f.write(f"\nProcesses:\n{procs}\n")
    f.write(f"\nFrontend size: {fsize}\n")
    f.write(f"\nNginx errors:\n{nerr}\n")
    f.write(f"\nBackend: {blog}\n")

ssh.close()
print("Done")
