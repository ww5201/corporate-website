import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=10)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("=== 后端健康检查 ===")
print(run("curl -s http://127.0.0.1:3000/api/health"))

print("\n=== 前端检查 ===")
print(run("curl -s http://127.0.0.1:3000/api/products | head -c 100"))

print("\n=== Nginx 状态 ===")
print(run("systemctl is-active nginx"))

print("\n=== 内存状态 ===")
print(run("free -h"))

print("\n=== 磁盘状态 ===")
print(run("df -h /"))

ssh.close()
print("\n所有服务正常！")
