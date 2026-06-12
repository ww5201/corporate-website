import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()

# Upload privacy.html
sftp.put(r'D:\tokai\privacy.html', '/var/www/frontend/privacy.html')
print('OK: privacy.html uploaded')

# Check current index.html footer area for adding privacy link
f = sftp.file('/var/www/frontend/index.html', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Find footer or bottom section
for i, line in enumerate(content.split('\n')):
    if 'footer' in line.lower() or 'bottom' in line.lower() or 'copyright' in line.lower() or '备案' in line or '版权' in line:
        start = max(0, i-2)
        end = min(len(content.split('\n')), i+5)
        print(f'--- Line {i+1} ---')
        for j in range(start, end):
            print(f'{j+1}: {content.split(chr(10))[j]}')
        print()

sftp.close()
ssh.close()
