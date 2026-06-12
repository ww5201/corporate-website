import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd, timeout=10):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
    except:
        out = ''
    return out

# 启动后端（不读取输出，避免超时）
ssh.exec_command("cd /root/backend && nohup node server-v4.js > /tmp/backend.log 2>&1 &")
time.sleep(4)

# 健康检查
health = run('curl -s http://localhost:3000/api/health')
print(f'Health: {health}')

# 前端
front = run('curl -s http://127.0.0.1/ | head -1')
print(f'Frontend OK: {"卓翌" in front or "html" in front}')

# 端口
port = run('ss -tlnp | grep :3000')
print(f'Port 3000: {port}')

ssh.close()
print('Done!')
