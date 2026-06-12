import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 内存使用情况
stdin, stdout, stderr = ssh.exec_command("free -h")
mem = stdout.read().decode('utf-8', errors='replace')

# 内存占用前10的进程
stdin, stdout, stderr = ssh.exec_command("ps aux --sort=-%mem | head -12")
procs = stdout.read().decode('utf-8', errors='replace')

# MySQL内存
stdin, stdout, stderr = ssh.exec_command("ps aux | grep mysql | grep -v grep | awk '{print $6/1024 \" MB - \" $11}'")
mysql = stdout.read().decode('utf-8', errors='replace').strip()

# Swap使用
stdin, stdout, stderr = ssh.exec_command("swapon --show")
swap = stdout.read().decode('utf-8', errors='replace')

with open(r'D:\tokai\memory_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Memory ===\n{mem}\n\n")
    f.write(f"=== Top Processes ===\n{procs}\n\n")
    f.write(f"=== MySQL ===\n{mysql}\n\n")
    f.write(f"=== Swap ===\n{swap}")

ssh.close()
print("Done")
