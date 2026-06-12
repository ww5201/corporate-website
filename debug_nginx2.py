import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check what's listening on port 80
stdin, stdout, stderr = ssh.exec_command('ss -tlnp | grep ":80"')
result1 = stdout.read().decode()

# Check nginx config
stdin, stdout, stderr = ssh.exec_command('cat /etc/nginx/conf.d/site.conf')
result2 = stdout.read().decode()

# Check if there's another web server
stdin, stdout, stderr = ssh.exec_command('systemctl list-units --type=service | grep -i "httpd\\|apache\\|nginx"')
result3 = stdout.read().decode()

# Check nginx status
stdin, stdout, stderr = ssh.exec_command('systemctl status nginx')
result4 = stdout.read().decode()

with open('D:/tokai/nginx_debug.txt', 'w', encoding='utf-8') as f:
    f.write("=== Port 80 ===\n" + result1 + "\n\n")
    f.write("=== site.conf ===\n" + result2 + "\n\n")
    f.write("=== Web servers ===\n" + result3 + "\n\n")
    f.write("=== Nginx status ===\n" + result4)

ssh.close()
print("Done")
