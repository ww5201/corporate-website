import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
for f in sftp.listdir('/var/www/frontend/'):
    print(f)

sftp.close()
ssh.close()
