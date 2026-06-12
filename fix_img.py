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
with sftp.file("/var/www/frontend/index.html", "w") as f:
    f.write(content)

print(f"已上传: {len(content)} 字符")

# 验证
stdin, stdout, stderr = client.exec_command("grep 'const IMG' /var/www/frontend/index.html")
print(stdout.read().decode().strip())

sftp.close()
client.close()
print("完成!")
