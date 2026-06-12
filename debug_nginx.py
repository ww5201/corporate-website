import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查所有nginx配置
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/nginx.conf")
nginx_main = stdout.read().decode('utf-8', errors='replace')

# 检查所有conf.d
stdin, stdout, stderr = ssh.exec_command("ls -la /etc/nginx/conf.d/ && echo '---' && cat /etc/nginx/conf.d/*.conf 2>/dev/null")
confs = stdout.read().decode('utf-8', errors='replace')

# 直接用curl带-H检查
stdin, stdout, stderr = ssh.exec_command("curl -s -H 'Cache-Control: no-cache' http://127.0.0.1/ | head -3")
curl2 = stdout.read().decode('utf-8', errors='replace')

# 用wget或直接读文件对比
stdin, stdout, stderr = ssh.exec_command("md5sum /var/www/frontend/index.html")
md5 = stdout.read().decode('utf-8', errors='replace')

# 检查是否有其他index.html
stdin, stdout, stderr = ssh.exec_command("find /var/www -name 'index.html' -exec md5sum {} \\;")
all_idx = stdout.read().decode('utf-8', errors='replace')

with open(r'D:\tokai\nginx_debug.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Nginx main conf ===\n{nginx_main}\n\n")
    f.write(f"=== All conf.d ===\n{confs}\n\n")
    f.write(f"=== Curl no-cache ===\n{curl2}\n\n")
    f.write(f"=== MD5 ===\n{md5}\n\n")
    f.write(f"=== All index.html ===\n{all_idx}")

ssh.close()
print("Done")
