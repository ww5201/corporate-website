import paramiko

# 上传 admin.html 到服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\admin.html', '/root/backend/admin.html')
sftp.put(r'D:\tokai\admin.html', '/var/www/frontend/admin.html')
sftp.close()
ssh.close()
print("Admin.html uploaded!")
