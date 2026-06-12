import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查前端文件
stdin, stdout, stderr = ssh.exec_command("head -30 /var/www/frontend/index.html")
content = stdout.read().decode('utf-8', errors='replace')

# 检查文件大小
stdin, stdout, stderr = ssh.exec_command("wc -c /var/www/frontend/index.html")
size = stdout.read().decode('utf-8', errors='replace').strip()

# 检查 nginx 状态
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/")
nginx = stdout.read().decode('utf-8', errors='replace').strip()

# 检查后端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()

ssh.close()

with open(r'D:\tokai\check_result2.txt', 'w', encoding='utf-8') as f:
    f.write(f"Nginx: {nginx}\n")
    f.write(f"Backend: {health}\n")
    f.write(f"File size: {size}\n\n")
    f.write(f"First 30 lines:\n{content}")

print("Done")
