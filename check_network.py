import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 1. 检查nginx是否运行
nginx = run("systemctl is-active nginx")
print(f"Nginx: {nginx}")

# 2. 检查后端是否运行
health = run("curl -s http://localhost:3000/api/health")
print(f"Backend: {health}")

# 3. 检查端口监听
ports = run("ss -tlnp | grep -E ':80|:443|:3000'")
print(f"Ports:\n{ports}")

# 4. 检查防火墙
firewall = run("systemctl is-active firewalld 2>/dev/null || echo 'not running'")
print(f"Firewalld: {firewall}")

# 5. 检查iptables
iptables = run("iptables -L -n 2>/dev/null | head -20")
print(f"Iptables:\n{iptables}")

# 6. 检查外网IP
ext_ip = run("curl -s ifconfig.me 2>/dev/null || curl -s ip.sb 2>/dev/null")
print(f"External IP: {ext_ip}")

# 7. 测试从服务器访问自己
self_test = run("curl -s -o /dev/null -w '%{http_code}' http://8.138.218.146/ 2>/dev/null")
print(f"Self access: {self_test}")

ssh.close()
