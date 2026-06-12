import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 直接测试后端3000端口的图片
print('=== 后端3000端口图片测试 ===')
print(run('curl -sI http://127.0.0.1:3000/uploads/1779850816993-ql0rh1icf.png'))

# 检查uploads目录
print('\n=== uploads目录 ===')
print(run('ls -la /root/backend/uploads/'))

# 检查文件是否真实存在且是图片
print('\n=== 文件类型检查 ===')
print(run('file /root/backend/uploads/1779850816993-ql0rh1icf.png'))

# 检查后端进程
print('\n=== 后端进程 ===')
print(run('ps aux | grep node'))

# 检查server-v4.js中的静态文件配置
print('\n=== server.js静态文件配置 ===')
print(run('grep -n "static\\|uploads" /root/backend/server-v4.js'))

ssh.close()
