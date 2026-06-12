import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command("grep 'upload.array' /root/backend/server-v4.js")
print(f"Multer config: {stdout.read().decode().strip()}")

stdin, stdout, stderr = ssh.exec_command("grep -c '20' /root/backend/admin.html")
print(f"'20' count in admin: {stdout.read().decode().strip()}")

stdin, stdout, stderr = ssh.exec_command("grep '最多' /root/backend/admin.html")
print(f"Admin label: {stdout.read().decode().strip()}")

# 测试API
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/products | head -c 200")
print(f"Products API: {stdout.read().decode().strip()}")

ssh.close()

ssh.close()
