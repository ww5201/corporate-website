import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()
ssh.close()

# Get the selectPay context
idx = html.find('selectPay')
context = html[idx-200:idx+1000]

with open('D:/tokai/payment_detail.txt', 'w', encoding='utf-8') as f:
    f.write(f"Context around selectPay (pos {idx}):\n\n{context}\n")

print("Done")
