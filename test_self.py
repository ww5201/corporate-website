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

# 从服务器访问自己的公网IP
test = run("curl -s --max-time 3 -o /dev/null -w '%{http_code}' http://8.138.218.146/ 2>/dev/null")
print(f"Self access via public IP: {test}")

# 检查是否有其他nginx配置干扰
other_conf = run("ls /etc/nginx/conf.d/")
print(f"Nginx conf files: {other_conf}")

# 检查nginx是否监听所有接口
listen = run("ss -tlnp | grep :80")
print(f"Port 80 listen: {listen}")

# 检查安全组是否真的生效（查看是否有其他限制）
# 尝试从外部测试
print("\nTesting from local machine...")

ssh.close()
print("Done")
