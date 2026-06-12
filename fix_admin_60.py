import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 修改admin.html中的图片限制 20->60
cmds = [
    "sed -i 's/imgUrls.length + files.length > 20/imgUrls.length + files.length > 60/g' /root/backend/admin.html",
    "sed -i 's/最多只能上传20张图片/最多只能上传60张图片/g' /root/backend/admin.html",
]

for cmd in cmds:
    ssh.exec_command(cmd)

# 验证修改
stdin, stdout, stderr = ssh.exec_command("grep -n '60' /root/backend/admin.html | grep -i 'image\\|img\\|pic\\|upload\\|最多\\|max\\|files\\|length'")
result = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Updated lines: {result}")

# 同步到前端目录
ssh.exec_command("cp /root/backend/admin.html /var/www/frontend/admin.html")

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
