import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 备份旧文件
stdin, stdout, stderr = client.exec_command("cp /var/www/frontend/index.html /var/www/frontend/index.html.bak")
print("已备份旧文件")

# 上传新文件
with open("D:/tokai/index-new.html", "r", encoding="utf-8") as f:
    new_content = f.read()

# 通过SFTP上传
sftp = client.open_sftp()
with sftp.file("/var/www/frontend/index.html", "w") as remote_file:
    remote_file.write(new_content)

print(f"已上传新文件: {len(new_content)} 字符")

# 检查文件
stdin, stdout, stderr = client.exec_command("ls -la /var/www/frontend/index.html")
print(stdout.read().decode())

sftp.close()
client.close()
print("完成！")
