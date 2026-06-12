import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

output_file = "D:/tokai/frontend_files.txt"
with open(output_file, "w", encoding="utf-8") as f:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, port, user, pwd, timeout=10)
        f.write("=== 查找前端文件 ===\n\n")
        
        # 查找所有HTML文件
        stdin, stdout, stderr = client.exec_command("find /root /var/www -name '*.html' 2>/dev/null | head -20")
        f.write("HTML文件:\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看 /var/www 目录
        stdin, stdout, stderr = client.exec_command("ls -la /var/www/")
        f.write("\n/var/www/:\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看是否有 frontend 目录
        stdin, stdout, stderr = client.exec_command("find /var/www -type f -name '*.html' -o -name '*.js' -o -name '*.css' 2>/dev/null | head -30")
        f.write("\n前端相关文件:\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看 nginx 配置
        stdin, stdout, stderr = client.exec_command("ls -la /etc/nginx/conf.d/ 2>/dev/null || ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo 'no nginx'")
        f.write("\nNginx配置:\n")
        f.write(stdout.read().decode())
        
    except Exception as e:
        f.write(f"Error: {e}\n")
    finally:
        client.close()
