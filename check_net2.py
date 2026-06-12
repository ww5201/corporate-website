import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd, timeout=5):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    try:
        return stdout.read().decode('utf-8', errors='replace').strip()
    except:
        return "timeout"

# 检查网络接口
net = run("ip addr show | grep 'inet ' | grep -v 127.0.0.1")
print(f"Network:\n{net}")

# 检查默认路由
route = run("ip route show default")
print(f"Default route: {route}")

# 检查DNS
dns = run("cat /etc/resolv.conf | head -3")
print(f"DNS:\n{dns}")

# 测试外网连接
ping = run("ping -c 1 -W 2 8.8.8.8 2>&1 | tail -2")
print(f"Ping: {ping}")

ssh.close()
