import paramiko, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=10)

def run(cmd, t=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=t)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

print("=== 当前 Swap ===")
out, _ = run("free -h | grep Swap")
print(out or "No swap")

# 创建 2GB Swap
print("\n=== 创建 2GB Swap 文件 ===")
out, err = run("dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress")
print(f"创建完成：{out[-100:] if out else 'done'}")

print("\n=== 设置权限 ===")
run("chmod 600 /swapfile")

print("\n=== 格式化为 Swap ===")
out, _ = run("mkswap /swapfile")
print(out)

print("\n=== 启用 Swap ===")
run("swapon /swapfile")

print("\n=== 设置开机自动挂载 ===")
run("grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab")

print("\n=== 验证 Swap ===")
out, _ = run("free -h")
print(out)

# 设置 swappiness (降低 Swap 使用倾向)
print("\n=== 优化 Swap 策略 ===")
run("sysctl vm.swappiness=10")
run("grep -q 'vm.swappiness=10' /etc/sysctl.conf || echo 'vm.swappiness=10' >> /etc/sysctl.conf")

print("\n=== 最终状态 ===")
out, _ = run("free -h")
print(out)

ssh.close()
print("\nSwap 创建成功！")
