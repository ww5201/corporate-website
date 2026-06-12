import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 1. 查看谁在监听80端口
stdin, stdout, stderr = client.exec_command("ss -tlnp | grep ':80 '")
print("=== 80端口监听者 ===")
print(stdout.read().decode())

# 2. 查看所有web相关进程
stdin, stdout, stderr = client.exec_command("ps aux | grep -E 'nginx|apache|httpd|python.*http|node.*3000' | grep -v grep")
print("=== Web进程 ===")
print(stdout.read().decode())

# 3. 查看nginx实际配置
stdin, stdout, stderr = client.exec_command("nginx -T 2>&1 | head -100")
print("=== Nginx完整配置 ===")
print(stdout.read().decode())

# 4. 直接curl localhost看看返回什么
stdin, stdout, stderr = client.exec_command("curl -s http://127.0.0.1:80 | head -30")
print("=== localhost:80 返回 ===")
print(stdout.read().decode())

# 5. 检查是否有默认页面
stdin, stdout, stderr = client.exec_command("ls -la /usr/share/nginx/html/ 2>/dev/null || echo '不存在'")
print("=== 默认页面目录 ===")
print(stdout.read().decode())

# 6. 看看frontend index.html内容
stdin, stdout, stderr = client.exec_command("head -8 /var/www/frontend/index.html")
print("=== /var/www/frontend/index.html ===")
print(stdout.read().decode())

# 7. 检查nginx conf.d是否有默认配置冲突
stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/conf.d/ && cat /etc/nginx/nginx.conf | grep -A5 'include'")
print("=== Nginx主配置include ===")
print(stdout.read().decode())

client.close()
