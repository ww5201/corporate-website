import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()

# 1. 上传 server-v4.js
print('=== 上传 server-v4.js ===')
sftp.put(r'D:\tokai\backend\server-v4.js', '/root/backend/server-v4.js')
print('OK')

# 2. 上传 admin.html
print('=== 上传 admin.html ===')
sftp.put(r'D:\tokai\backend\admin-v2.html', '/root/backend/admin.html')
print('OK')

# 3. 上传前端文件
print('=== 上传前端文件 ===')
dist = r'D:\tokai\dist'
for root, dirs, files in os.walk(dist):
    for f in files:
        local = os.path.join(root, f)
        rel = os.path.relpath(local, dist).replace('\\', '/')
        remote = '/var/www/frontend/' + rel
        sftp.put(local, remote)
        print(f'  {rel}')

sftp.close()

# 4. 重启后端
print('=== 重启后端 ===')
stdin, stdout, stderr = ssh.exec_command('pkill -f "node server-v4.js" 2>/dev/null; sleep 1; cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 &', timeout=10)
print('PID:', stdout.read().decode().strip())

# 5. 重载nginx
print('=== 重载nginx ===')
stdin, stdout, stderr = ssh.exec_command('systemctl reload nginx', timeout=10)
print(stderr.read().decode().strip() or 'OK')

# 6. 验证
import time
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/health', timeout=10)
print('=== 健康检查 ===')
print(stdout.read().decode().strip())

ssh.close()
print('\n✅ 部署完成！')
