import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

stdin, stdout, stderr = ssh.exec_command('cat /root/backend/routes/auth.js')
content = stdout.read().decode('utf-8', errors='replace')

# Find wechat section
idx = content.find('wechat')
if idx >= 0:
    print(content[max(0,idx-100):idx+2000])
else:
    print("NO WECHAT SECTION FOUND")
    print("---LAST 1500 chars---")
    print(content[-1500:])

ssh.close()
