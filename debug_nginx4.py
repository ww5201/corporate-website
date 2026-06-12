import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check if there's another server on port 80
stdin, stdout, stderr = ssh.exec_command('ss -tlnp | grep ":80"')
port80 = stdout.read().decode()

# Check if apache is installed
stdin, stdout, stderr = ssh.exec_command('rpm -qa | grep -i httpd; dpkg -l | grep -i apache 2>/dev/null || echo "check rpm only"')
apache = stdout.read().decode()

# Check if there's a firewall redirect
stdin, stdout, stderr = ssh.exec_command('iptables -t nat -L -n 2>/dev/null | head -20')
iptables = stdout.read().decode()

# Check if any other process is using port 80
stdin, stdout, stderr = ssh.exec_command('netstat -tlnp | grep ":80"')
netstat = stdout.read().decode()

# Check nginx error log
stdin, stdout, stderr = ssh.exec_command('tail -20 /var/log/nginx/error.log')
errors = stdout.read().decode()

# Check nginx access log for the browser request
stdin, stdout, stderr = ssh.exec_command('tail -20 /var/log/nginx/access.log')
access = stdout.read().decode()

with open('D:/tokai/nginx_debug3.txt', 'w', encoding='utf-8') as f:
    f.write("=== Port 80 listeners ===\n" + port80 + "\n\n")
    f.write("=== Apache/HTTPD packages ===\n" + apache + "\n\n")
    f.write("=== iptables NAT ===\n" + iptables + "\n\n")
    f.write("=== netstat ===\n" + netstat + "\n\n")
    f.write("=== nginx error log ===\n" + errors + "\n\n")
    f.write("=== nginx access log ===\n" + access)

ssh.close()
print("Done")
