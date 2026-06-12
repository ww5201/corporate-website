import paramiko
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = c.open_sftp()
f = sftp.file('/root/backend/server-v4.js', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

lines = content.split('\n')
for i, line in enumerate(lines):
    if any(kw in line for kw in ['auth/sms', 'auth/phone', 'auth/wechat', 'sms/send']):
        start = max(0, i-2)
        end = min(len(lines), i+5)
        print(f'--- Line {i+1} ---')
        for j in range(start, end):
            print(f'{j+1}: {lines[j]}')
        print()
c.close()
