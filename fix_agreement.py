import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
f = sftp.file('/var/www/frontend/login.html', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Directly replace all javascript:void(0) links with privacy.html
content = content.replace('href="javascript:void(0)"', 'href="/privacy.html"')

f = sftp.file('/var/www/frontend/login.html', 'w')
f.write(content)
f.close()

# Verify
f = sftp.file('/var/www/frontend/login.html', 'r')
content2 = f.read().decode('utf-8', errors='ignore')
f.close()

lines = content2.split('\n')
for i, line in enumerate(lines):
    if 'void(0)' in line or 'agreement' in line.lower():
        safe = lines[i].encode('ascii', 'replace').decode('ascii')
        print(f'{i+1}: {safe}')

print('Done')

sftp.close()
ssh.close()
