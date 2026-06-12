import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download and compare
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    remote = f.read().decode('utf-8')
sftp.close()

with open(r'D:/tokai/index-final-settings.html', 'r', encoding='utf-8', errors='surrogatepass') as f:
    local = f.read()

print(f"Local: {len(local)}")
print(f"Remote: {len(remote)}")
print(f"Match: {local == remote}")

# Check mobile nav
m = remote.find('<nav class="mobile-nav">')
if m >= 0:
    me = remote.find('</nav>', m) + 6
    has = '\u2699' in remote[m:me]
    print(f"Mobile settings: {has}")

ssh.close()
