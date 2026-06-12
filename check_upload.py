import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 读取服务器上的文件内容
stdin, stdout, stderr = client.exec_command("cat /var/www/frontend/index.html")
server_content = stdout.read().decode()

# 读取本地文件
with open("D:/tokai/index-v3.html", "r", encoding="utf-8") as f:
    local_content = f.read()

print(f"服务器文件大小: {len(server_content)}")
print(f"本地文件大小: {len(local_content)}")

# 检查是否包含 hero-slide
print(f"服务器包含 hero-slide: {'hero-slide' in server_content}")
print(f"本地包含 hero-slide: {'hero-slide' in local_content}")

# 检查前100个字符
print(f"\n服务器前100字符: {server_content[:100]}")
print(f"本地前100字符: {local_content[:100]}")

# 检查是否有 Vite 引用
print(f"服务器包含 assets: {'assets' in server_content}")
print(f"本地包含 assets: {'assets' in local_content}")

# 直接用 cat 重新写入
stdin, stdout, stderr = client.exec_command("cat /dev/null > /var/www/frontend/index.html && echo 'cleared'")
print(f"\n清空结果: {stdout.read().decode()}")

# 用 sftp 重新上传
sftp = client.open_sftp()
with sftp.file("/var/www/frontend/index.html", "w") as remote:
    remote.write(local_content)

# 验证
stdin, stdout, stderr = client.exec_command("wc -c /var/www/frontend/index.html")
print(f"重新上传后大小: {stdout.read().decode().strip()}")

# 再次检查内容
stdin, stdout, stderr = client.exec_command("head -20 /var/www/frontend/index.html")
print("\n新文件前20行:")
print(stdout.read().decode())

sftp.close()
client.close()
