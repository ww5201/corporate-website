import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 读取当前文件
stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8')

# 把 tel: 链接改成 onclick 调用 Android JS桥接
old = '<a href="tel:18977122166" style="color:inherit;text-decoration:none">18977122166</a>'
new = '<a href="tel:18977122166" style="color:inherit;text-decoration:none" onclick="if(window.Android){Android.callPhone(\'18977122166\');return false;}">18977122166</a>'

count_before = html.count(old)
html = html.replace(old, new)
print(f"Updated tel links: {count_before}")

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
stdin, stdout, stderr = ssh.exec_command("grep -c 'Android.callPhone' /var/www/frontend/index.html")
c = stdout.read().decode().strip()
print(f"JS bridge refs: {c}")

ssh.close()
print("Done!")
