import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

with open("D:/tokai/index-v3.html", "r", encoding="utf-8") as f:
    content = f.read()

sftp = client.open_sftp()
with sftp.file("/var/www/frontend/index.html", "w") as remote:
    remote.write(content)

print(f"已上传: {len(content)} 字符")

# 同时删除 assets 目录，避免干扰
stdin, stdout, stderr = client.exec_command("rm -rf /var/www/frontend/assets")
print("已删除 assets 目录")

# 验证
stdin, stdout, stderr = client.exec_command("ls -la /var/www/frontend/")
print(stdout.read().decode())

sftp.close()
client.close()
print("完成!")
