import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 验证后端
stdin, stdout, stderr = ssh.exec_command("grep 'upload.array' /root/backend/server-v4.js")
backend = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Backend upload: {backend}")

# 检查admin.html中的20/60
stdin, stdout, stderr = ssh.exec_command("grep -c '60' /root/backend/admin.html")
c60 = stdout.read().decode('utf-8', errors='replace').strip()
stdin, stdout, stderr = ssh.exec_command("grep -c '20' /root/backend/admin.html")
c20 = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Admin 60 count: {c60}, 20 count: {c20}")

# 也改前端目录
ssh.exec_command("cp /root/backend/admin.html /var/www/frontend/admin.html")
print("Copied admin.html to frontend")

# 重启后端
ssh.exec_command("pkill -f 'node server-v4.js'")
import time
time.sleep(1)
ssh.exec_command("cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 &")
time.sleep(2)

# 验证
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Health: {health}")

ssh.close()
print("Done!")
