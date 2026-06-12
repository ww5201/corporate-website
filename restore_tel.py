import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 读取当前文件
stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8')

# 把 onclick 改回 tel: 链接
old = '<span style="color:inherit;cursor:pointer" onclick="callPhone()">18977122166</span>'
new = '<a href="tel:18977122166" style="color:inherit;text-decoration:none">18977122166</a>'

count_before = html.count(old)
html = html.replace(old, new)
print(f"Restored tel: links: {count_before}")

# 写回服务器
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

ssh.exec_command("nginx -s reload")

# 同步到本地
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 验证
stdin, stdout, stderr = ssh.exec_command("grep -c 'tel:18977122166' /var/www/frontend/index.html")
c = stdout.read().decode().strip()
print(f"Total tel: links on server: {c}")

ssh.close()
print("Done!")
