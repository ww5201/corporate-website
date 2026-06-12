import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 1. 检查 nginx 配置，看静态文件怎么映射的
stdin, stdout, stderr = client.exec_command("cat /etc/nginx/conf.d/site.conf")
print("=== Nginx 配置 ===")
print(stdout.read().decode())

# 2. 检查前端目录实际文件
stdin, stdout, stderr = client.exec_command("ls -la /var/www/frontend/")
print("\n=== 前端目录 ===")
print(stdout.read().decode())

# 3. 检查 backend 的 uploads 目录
stdin, stdout, stderr = client.exec_command("ls -la /root/backend/uploads/ 2>/dev/null || echo '目录不存在'")
print("\n=== uploads 目录 ===")
print(stdout.read().decode())

# 4. 检查当前 index.html 的前50行
stdin, stdout, stderr = client.exec_command("head -50 /var/www/frontend/index.html")
print("\n=== index.html 前50行 ===")
print(stdout.read().decode())

# 5. 查看 nginx 是否在运行
stdin, stdout, stderr = client.exec_command("ps aux | grep nginx | grep -v grep")
print("\n=== Nginx 进程 ===")
print(stdout.read().decode())

# 6. 查看 backend 是否在运行
stdin, stdout, stderr = client.exec_command("ps aux | grep node | grep -v grep")
print("\n=== Node 进程 ===")
print(stdout.read().decode())

client.close()
