import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查所有监听端口
stdin, stdout, stderr = ssh.exec_command("netstat -tlnp | grep -E ':(80|3000|443|8080) '")
ports = stdout.read().decode('utf-8', errors='replace')

# 用curl直接访问网站看返回什么
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1/ | head -30")
curl_out = stdout.read().decode('utf-8', errors='replace')

# 检查index.html实际内容
stdin, stdout, stderr = ssh.exec_command("wc -c /var/www/frontend/index.html && head -5 /var/www/frontend/index.html")
idx_info = stdout.read().decode('utf-8', errors='replace')

# 检查是否有其他web服务
stdin, stdout, stderr = ssh.exec_command("systemctl list-units --type=service --state=running | grep -E 'nginx|apache|httpd'")
services = stdout.read().decode('utf-8', errors='replace')

# 检查root目录下有没有视频相关的东西
stdin, stdout, stderr = ssh.exec_command("ls -la /root/*.html /root/*.htm /root/index* 2>/dev/null; ls -la /var/www/ 2>/dev/null")
www_root = stdout.read().decode('utf-8', errors='replace')

with open(r'D:\tokai\deep_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== Listening ports ===\n{ports}\n\n")
    f.write(f"=== Curl output ===\n{curl_out}\n\n")
    f.write(f"=== Index info ===\n{idx_info}\n\n")
    f.write(f"=== Running services ===\n{services}\n\n")
    f.write(f"=== WWW root ===\n{www_root}")

ssh.close()
print("Done")
