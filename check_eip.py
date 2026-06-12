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

# 检查公网IP
ext = run("curl -s --max-time 3 http://100.100.100.200/latest/meta-data/eipv4 2>/dev/null")
print(f"EIP: {ext}")

# 检查所有IP
ips = run("hostname -I")
print(f"All IPs: {ips}")

# 检查是否能访问外网
web = run("curl -s --max-time 3 -o /dev/null -w '%{http_code}' http://www.baidu.com 2>/dev/null")
print(f"Baidu: {web}")

# 检查nginx配置
nginx_conf = run("cat /etc/nginx/conf.d/site.conf | head -20")
print(f"Nginx conf:\n{nginx_conf}")

ssh.close()
