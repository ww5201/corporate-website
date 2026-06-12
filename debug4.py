import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 检查default.conf
print('=== default.conf内容 ===')
print(run('cat /etc/nginx/conf.d/default.conf'))

# 检查nginx主配置
print('\n=== nginx主配置关键部分 ===')
print(run('cat /etc/nginx/nginx.conf'))

# 测试直接通过端口3000访问图片
print('\n=== 直接测试3000端口 ===')
print(run('curl -sI http://127.0.0.1:3000/uploads/1779850816993-ql0rh1icf.png | head -5'))

# 测试nginx是否真的代理了
print('\n=== 测试nginx代理 ===')
print(run('curl -sI http://127.0.0.1:80/uploads/1779850816993-ql0rh1icf.png | head -5'))

ssh.close()
