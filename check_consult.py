import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find product consult button
with open('D:/tokai/check_consult.txt', 'w', encoding='utf-8') as out:
    # Search for consult-related text in product rendering
    for keyword in ['咨询', 'consult', 'openOrder', 'contact-btn']:
        idx = html.find(keyword)
        if idx > 0:
            out.write(f"\n=== {keyword} at {idx} ===\n")
            out.write(html[max(0,idx-200):idx+200])
            out.write('\n')

ssh.close()
print("Done")
