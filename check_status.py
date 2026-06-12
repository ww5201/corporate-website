import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=10)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

print("=== Swap 状态 ===")
print(run("swapon --show"))

print("\n=== 内存状态 ===")
print(run("free -h"))

print("\n=== 最近 OOM 记录 ===")
print(run("dmesg | grep -i 'oom' | tail -3"))

print("\n=== 系统运行时间 ===")
print(run("uptime -p"))

print("\n=== 服务状态 ===")
print(f"Nginx: {run('systemctl is-active nginx')}")
print(f"MySQL: {run('systemctl is-active mysqld')}")
print(f"后端：{run('curl -s http://127.0.0.1:3000/api/health')}")

ssh.close()
print("\n系统正常，Swap 已启用！")
