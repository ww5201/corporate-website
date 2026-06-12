import paramiko

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\chat.html', '/var/www/frontend/chat.html')
sftp.close()

# Verify
stdin, out, err = ssh.exec_command('grep -n "msg-row" /var/www/frontend/chat.html | head -5')
print("Server chat.html now has:")
print(out.read().decode())

# Also check if backend serves chat.html
stdin2, out2, err2 = ssh.exec_command('grep -c "justify-content" /var/www/frontend/chat.html')
print("justify-content count:", out2.read().decode().strip())

ssh.close()
print('Done - chat.html deployed!')
