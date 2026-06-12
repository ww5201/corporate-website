import paramiko
import time

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

def run(cmd):
    print(f'>>> {cmd}')
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out: print(out.strip())
    if err: print(err.strip())
    print()
    return out, err

# 上传文件
print('=== 上传文件 ===')
sftp.put(r'D:\tokai\backend\server-v4.js', '/root/backend/server-v4.js')
print('server-v4.js uploaded')
sftp.put(r'D:\tokai\backend\admin-v2.html', '/root/backend/admin.html')
print('admin.html uploaded')

# 安装 multer
print('\n=== 安装 multer ===')
run('cd /root/backend && npm install multer 2>&1')

# 停止旧服务
print('\n=== 停止旧服务 ===')
run('pkill -f "node server" 2>/dev/null || true')
time.sleep(1)

# 启动新服务
print('\n=== 启动新服务 ===')
run('cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 &')
time.sleep(2)

# 验证
print('\n=== 验证 ===')
run('curl -s http://localhost:3000/api/health')
run('curl -s http://localhost:3000/api/products')

sftp.close()
ssh.close()
print('\nDone!')
