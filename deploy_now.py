import paramiko
import os
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

HOST = '8.138.218.146'
USER = 'root'
PWD = 'ww0987654.'

print('=' * 50)
print('  全部部署 - 前端 + 后端')
print('=' * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PWD, timeout=15)
sftp = ssh.open_sftp()

# 1. 上传后端文件
print('\n[1/4] 上传后端文件...')
backend_files = [
    (r'D:\tokai\backend\server-v4.js', '/root/backend/server-v4.js'),
    (r'D:\tokai\backend\admin.html',   '/root/backend/admin.html'),
    (r'D:\tokai\backend\shop.html',    '/root/backend/shop.html'),
    (r'D:\tokai\backend\login.html',   '/root/backend/login.html'),
    (r'D:\tokai\backend\payment.html', '/root/backend/payment.html'),
    (r'D:\tokai\backend\sms-service.js', '/root/backend/sms-service.js'),
    (r'D:\tokai\backend\routes\auth.js',    '/root/backend/routes/auth.js'),
    (r'D:\tokai\backend\routes\payment.js', '/root/backend/routes/payment.js'),
]

for local, remote in backend_files:
    if os.path.exists(local):
        sftp.put(local, remote)
        size = os.path.getsize(local)
        print(f'  ✓ {os.path.basename(local)} → {remote}  ({size:,} bytes)')
    else:
        print(f'  ✗ {local} 不存在，跳过')

# 2. 上传前端 dist/
print('\n[2/4] 上传前端文件...')
dist_dir = r'D:\tokai\dist'
upload_count = 0
for root, dirs, files in os.walk(dist_dir):
    for f in files:
        local = os.path.join(root, f)
        rel = os.path.relpath(local, dist_dir).replace('\\', '/')
        remote = '/var/www/frontend/' + rel
        # 确保远程目录存在
        remote_dir = os.path.dirname(remote).replace('\\', '/')
        try:
            sftp.stat(remote_dir)
        except FileNotFoundError:
            ssh.exec_command(f'mkdir -p {remote_dir}')
            time.sleep(0.3)
        sftp.put(local, remote)
        size = os.path.getsize(local)
        print(f'  ✓ {rel}  ({size:,} bytes)')
        upload_count += 1
print(f'  共上传 {upload_count} 个前端文件')

sftp.close()

# 3. 重启后端
print('\n[3/4] 重启后端服务...')
# 先检查当前运行的是哪个版本
stdin, stdout, stderr = ssh.exec_command('ps aux | grep "node server" | grep -v grep')
ps_out = stdout.read().decode().strip()
print(f'  当前进程: {ps_out or "无运行中的后端进程"}')

# 杀掉旧进程，启动新的
ssh.exec_command('pkill -f "node server-v" 2>/dev/null')
time.sleep(1)
stdin, stdout, stderr = ssh.exec_command(
    'cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 &'
)
time.sleep(3)

# 确认新进程启动
stdin, stdout, stderr = ssh.exec_command('ps aux | grep "node server-v4" | grep -v grep')
ps_new = stdout.read().decode().strip()
if ps_new:
    print(f'  ✓ server-v4.js 已启动')
else:
    print(f'  ⚠ 后端可能未启动，检查日志...')
    stdin, stdout, stderr = ssh.exec_command('tail -20 /tmp/backend.log')
    print(f'  日志: {stdout.read().decode().strip()}')

# 4. 更新前端导航（确保"我的"链接指向 /login.html）
print('\n[4/5] 更新前端导航...')
stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
fe_idx = stdout.read().decode('utf-8', errors='replace')
if '/login.html' not in fe_idx:
    old_nav = 'href="#contact" data-i18n="nav.contact">联系</a>\n    </div>'
    new_nav = 'href="#contact" data-i18n="nav.contact">联系</a>\n      <a href="/login.html" data-i18n="nav.profile">我的</a>\n    </div>'
    fe_idx = fe_idx.replace(old_nav, new_nav)
    sftp2 = ssh.open_sftp()
    with sftp2.open('/var/www/frontend/index.html', 'w') as f:
        f.write(fe_idx)
    sftp2.close()
    print('  ✓ 已添加"我的"导航链接')
else:
    print('  ✓ 导航已包含"我的"链接')

# 5. 重载 nginx
print('\n[5/5] 重载 nginx...')
stdin, stdout, stderr = ssh.exec_command('nginx -t 2>&1 && systemctl reload nginx 2>&1')
nginx_out = stdout.read().decode().strip()
nginx_err = stderr.read().decode().strip()
print(f'  {nginx_out or nginx_err or "OK"}')

# 5. 健康检查
print('\n' + '=' * 50)
print('  验证部署...')
print('=' * 50)
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health', timeout=10)
health_code = stdout.read().decode().strip()
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/health', timeout=10)
health_body = stdout.read().decode().strip()
print(f'  后端健康检查: HTTP {health_code}')
if health_body:
    print(f'  响应: {health_body}')

# 检查前端
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/', timeout=10)
fe_code = stdout.read().decode().strip()
print(f'  前端首页: HTTP {fe_code}')

ssh.close()
print('\n✅ 部署完成！')
print(f'  前端: http://{HOST}')
print(f'  后端: http://{HOST}:3000')
print(f'  管理后台: http://{HOST}:3000/admin.html')
print(f'  商城: http://{HOST}:3000/shop.html')
print(f'  登录: http://{HOST}/login.html')
print(f'  支付: http://{HOST}/payment.html')
