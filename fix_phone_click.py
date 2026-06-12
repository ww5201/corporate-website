import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 读取当前文件
stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8')

# 1. 联系卡片中的电话 - 加上 tel: 链接
old1 = '<p>18977122166</p>'
new1 = '<p><a href="tel:18977122166" style="color:inherit;text-decoration:none">18977122166</a></p>'
html = html.replace(old1, new1)

count1 = html.count(new1)
print(f"Contact card phone: {count1} replaced")

# 2. 检查是否还有其他地方的电话需要改（比如footer等）
old2 = '>18977122166<'
new2 = '><a href="tel:18977122166" style="color:inherit;text-decoration:none">18977122166</a><'
html = html.replace(old2, new2)
count2 = html.count(new2) - count1  # 减去已替换的
print(f"Other phone refs: {max(0, count2)} replaced")

# 写回服务器
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# 重载nginx
ssh.exec_command("nginx -s reload")

# 验证
stdin, stdout, stderr = ssh.exec_command("grep -c 'tel:18977122166' /var/www/frontend/index.html")
tel_count = stdout.read().decode().strip()
print(f"Total tel: links: {tel_count}")

ssh.close()
print("Done!")
