import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()
ssh.close()

# Find ALL occurrences of selectPay
import re
matches = [(m.start(), html[max(0,m.start()-50):m.start()+100]) for m in re.finditer('selectPay', html)]

with open('D:/tokai/payment_all.txt', 'w', encoding='utf-8') as f:
    f.write(f"Found {len(matches)} occurrences of selectPay:\n\n")
    for i, (pos, ctx) in enumerate(matches):
        f.write(f"--- #{i+1} at {pos} ---\n{ctx}\n\n")

print("Done")
