import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 先移除 assets 引用，只用内联版本
with open("D:/tokai/index-v2.html", "r", encoding="utf-8") as f:
    new_content = f.read()

sftp = client.open_sftp()
with sftp.file("/var/www/frontend/index.html", "w") as remote_file:
    remote_file.write(new_content)

print(f"已上传: {len(new_content)} 字符")

# 验证
stdin, stdout, stderr = client.exec_command("head -20 /var/www/frontend/index.html")
print(stdout.read().decode())

sftp.close()
client.close()
print("完成!")
