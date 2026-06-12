import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 检查文件大小和内容
stdin, stdout, stderr = client.exec_command("wc -c /var/www/frontend/index.html && head -5 /var/www/frontend/index.html && echo '---' && grep -c 'hero-slide' /var/www/frontend/index.html")
print("=== 文件状态 ===")
print(stdout.read().decode())

# 强制重新上传
sftp = client.open_sftp()
with open("D:/tokai/index-v3.html", "r", encoding="utf-8") as f:
    content = f.read()

# 先删除旧文件
client.exec_command("rm -f /var/www/frontend/index.html")

# 重新写入
with sftp.file("/var/www/frontend/index.html", "w") as remote:
    remote.write(content)

print(f"重新上传: {len(content)} 字符")

# 验证
stdin, stdout, stderr = client.exec_command("wc -c /var/www/frontend/index.html && head -5 /var/www/frontend/index.html")
print("上传后:")
print(stdout.read().decode())

# 清除 nginx 缓存（如果有的话）
client.exec_command("nginx -s reload")
print("Nginx 已重载")

sftp.close()
client.close()
