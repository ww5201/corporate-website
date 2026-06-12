import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 检查端口3000占用
stdin, stdout, stderr = ssh.exec_command("lsof -i :3000 | head -20")
port = stdout.read().decode('utf-8', errors='replace')

# 2. 检查所有node进程
stdin, stdout, stderr = ssh.exec_command("ps aux | grep node | grep -v grep")
nodes = stdout.read().decode('utf-8', errors='replace')

# 3. 检查nginx配置
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/conf.d/site.conf")
nginx_conf = stdout.read().decode('utf-8', errors='replace')

with open(r'D:\tokai\port_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Port 3000 ===\n{port}\n\n")
    f.write(f"=== Node processes ===\n{nodes}\n\n")
    f.write(f"=== Nginx config ===\n{nginx_conf}")

ssh.close()
print("Done")
