import paramiko
import os

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

# 上传 admin.html 到 /root/
local2 = r'D:\tokai\backend\admin.html'
remote2 = '/root/admin-new.html'
print(f'Uploading admin.html...')
sftp.put(local2, remote2)
print('Admin.html uploaded!')

# 执行部署命令
cmds = [
    'rm -rf /var/www/frontend/*',
    'unzip -o /root/frontend-new.zip -d /var/www/frontend/',
    'cp /root/admin-new.html /var/www/frontend/admin.html',
    'nginx -t && systemctl reload nginx',
]
for cmd in cmds:
    print(f'>>> {cmd}')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out: print(out)
    if err: print(err)
    print()

# 同时更新后端
cmds2 = [
    'mkdir -p /root/backend/admin',
    'cp /root/admin-new.html /root/backend/admin/admin.html',
]
for cmd in cmds2:
    print(f'>>> {cmd}')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out: print(out)
    if err: print(err)

# 重启后端
print('>>> 重启后端服务...')
stdin, stdout, stderr = ssh.exec_command('pkill -f "node server-v3.js" 2>/dev/null; cd /root/backend && nohup node server-v3.js > /tmp/backend.log 2>&1 &')
import time
time.sleep(2)

# 验证
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/health')
print('后端状态:', stdout.read().decode())

sftp.close()
ssh.close()
print('\n✅ 部署完成！')
print('前端: http://8.138.218.146')
print('管理后台: http://8.138.218.146:3000/admin.html')
