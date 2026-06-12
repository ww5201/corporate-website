import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 修改后端 server-v4.js - 上传限制 20 -> 60
stdin, stdout, stderr = ssh.exec_command("cd /root/backend && sed -i 's/upload.array(\"images\", 20)/upload.array(\"images\", 60)/g' server-v4.js && grep 'upload.array' server-v4.js")
backend = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Backend: {backend}")

# 2. 修改 admin.html - 图片限制 20 -> 60
stdin, stdout, stderr = ssh.exec_command("cd /root/backend && sed -i 's/>20/>60/g; s/max 20/max 60/g; s/最多20/最多60/g; s/最多 20/最多 60/g; s/最多可上传20/最多可上传60/g' admin.html")

# 验证admin修改
stdin, stdout, stderr = ssh.exec_command("cd /root/backend && grep -n '60\\|20' admin.html | grep -i 'image\\|img\\|pic\\|photo\\|max\\|最多' | head -10")
admin = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Admin: {admin}")

# 3. 重启后端
stdin, stdout, stderr = ssh.exec_command("pkill -f 'node server-v4.js'; sleep 1; cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 & echo $!")
ssh.exec_command("sleep 2")

# 4. 复制admin.html到前端目录
stdin, stdout, stderr = ssh.exec_command("cp /root/backend/admin.html /var/www/frontend/admin.html && echo copied")
copy = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Copy: {copy}")

# 5. 验证后端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Health: {health}")

ssh.close()
print("Done!")
