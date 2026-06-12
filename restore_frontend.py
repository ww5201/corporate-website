import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 上传前端文件
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()

# 重载 nginx
ssh.exec_command("nginx -s reload")

# 验证
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' http://localhost/")
code = stdout.read().decode('utf-8', errors='replace').strip()

stdin, stdout, stderr = ssh.exec_command("head -6 /var/www/frontend/index.html | tail -1")
title = stdout.read().decode('utf-8', errors='replace').strip()

ssh.close()
print(f"Nginx: {code}, Title line: {title}")
print("Done!")
