import paramiko
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = c.open_sftp()
try:
    f = sftp.file('/root/backend/sms-service.js', 'r')
    content = f.read().decode('utf-8', errors='ignore')
    f.close()
    print(content)
except Exception as e:
    print(f'FILE NOT FOUND: {e}')
c.close()
