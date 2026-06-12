import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 检查所有nginx配置
print('=== 所有nginx配置文件 ===')
print(run('ls -la /etc/nginx/conf.d/'))

# 检查默认配置
print('\n=== 默认server配置 ===')
print(run('cat /etc/nginx/nginx.conf | grep -A 20 "server {"'))

# 检查site.conf的完整内容
print('\n=== site.conf完整内容 ===')
print(run('cat /etc/nginx/conf.d/site.conf'))

# 测试nginx直接访问图片（不通过代理）
print('\n=== 测试nginx直接访问 ===')
print(run('curl -sI http://localhost/uploads/1779850816993-ql0rh1icf.png'))

# 检查nginx错误日志
print('\n=== nginx错误日志 ===')
print(run('tail -20 /var/log/nginx/error.log 2>/dev/null || echo no error log'))

# 检查nginx访问日志
print('\n=== nginx访问日志 ===')
print(run('tail -10 /var/log/nginx/access.log 2>/dev/null || echo no access log'))

ssh.close()
