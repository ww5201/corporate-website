import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. 删除 nextapps.conf
print("Deleting nextapps.conf...")
stdin, stdout, stderr = ssh.exec_command("rm /etc/nginx/conf.d/nextapps.conf && echo 'deleted' || echo 'failed'")
del_result = stdout.read().decode('utf-8').strip()
print(f"Delete: {del_result}")

# 2. 检查是否还有其他视频进程在跑
stdin, stdout, stderr = ssh.exec_command("lsof -i :3001 | head -5")
p3001 = stdout.read().decode('utf-8').strip()
print(f"Port 3001: {p3001 if p3001 else 'FREE'}")

# 3. 重载nginx
print("\nReloading nginx...")
ssh.exec_command("nginx -t && nginx -s reload")
import time
time.sleep(1)

# 4. 验证前端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1/ | head -3")
front = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\nFrontend now:\n{front[:200]}")

# 5. 验证后端
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/health")
health = stdout.read().decode('utf-8').strip()
print(f"\nBackend: {health}")

# 6. 确认nginx配置正确
stdin, stdout, stderr = ssh.exec_command("ls /etc/nginx/conf.d/")
confs = stdout.read().decode('utf-8').strip()
print(f"\nNginx confs: {confs}")

ssh.close()
print("\nDone!")
