import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check main nginx.conf
stdin, stdout, stderr = ssh.exec_command('cat /etc/nginx/nginx.conf')
main_conf = stdout.read().decode()

# Check default config
stdin, stdout, stderr = ssh.exec_command('ls /etc/nginx/conf.d/ && cat /etc/nginx/conf.d/*.conf 2>/dev/null')
conf_files = stdout.read().decode()

# Check if default site exists
stdin, stdout, stderr = ssh.exec_command('ls /etc/nginx/sites-enabled/ 2>/dev/null || echo "no sites-enabled"')
sites = stdout.read().decode()

# Check what curl returns on server
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1/ | head -5')
curl_result = stdout.read().decode()

# Check actual content of /var/www/frontend/
stdin, stdout, stderr = ssh.exec_command('ls -la /var/www/frontend/')
files = stdout.read().decode()

# Check if there's an index.html in /usr/share/nginx/html/
stdin, stdout, stderr = ssh.exec_command('ls /usr/share/nginx/html/ 2>/dev/null || echo "no default"')
default_dir = stdout.read().decode()

with open('D:/tokai/nginx_debug2.txt', 'w', encoding='utf-8') as f:
    f.write("=== nginx.conf ===\n" + main_conf + "\n\n")
    f.write("=== conf.d files ===\n" + conf_files + "\n\n")
    f.write("=== sites-enabled ===\n" + sites + "\n\n")
    f.write("=== curl localhost ===\n" + curl_result + "\n\n")
    f.write("=== /var/www/frontend/ ===\n" + files + "\n\n")
    f.write("=== default html dir ===\n" + default_dir)

ssh.close()
print("Done")
