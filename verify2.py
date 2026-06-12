import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 检查后端
print('=== 后端进程 ===')
print(run('ps aux | grep "server-v4" | grep -v grep'))

# 检查健康
time.sleep(1)
print('\n=== 健康检查 ===')
print(run('curl -s http://localhost:3000/api/health'))

# 检查支付配置
print('\n=== 支付配置API ===')
print(run('curl -s http://localhost:3000/api/payment-config'))

# 检查订单API
print('\n=== 订单API ===')
print(run('curl -s http://localhost:3000/api/orders'))

ssh.close()
