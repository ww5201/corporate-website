import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 上传后端
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\server-v4.js', '/root/backend/server-v4.js')
print("Backend uploaded")
sftp.close()

# 重启后端
print("Restarting backend...")
ssh.exec_command("pkill -f 'node server' 2>/dev/null")
time.sleep(2)
ssh.exec_command("cd /root/backend && nohup node server-v4.js > /tmp/server.log 2>&1 &")
time.sleep(3)

# 检查健康
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode().strip()
print(f"Health: {health}")

# 检查案例 API
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/cases")
cases = stdout.read().decode().strip()
print(f"Cases API: {cases}")

ssh.close()
print("Backend restarted successfully!")
