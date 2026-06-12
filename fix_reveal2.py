import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
html = stdout.read().decode('utf-8')

# Exact match for current CSS
old_css = '.reveal { opacity:0; transform:translateY(30px); transition: all 0.7s cubic-bezier(0.16,1,0.3,1); }'
new_css = '.reveal { opacity: 1 !important; transform: none !important; }'

if old_css in html:
    html = html.replace(old_css, new_css)
    print("FIXED: .reveal now always visible")
else:
    print("Pattern not found, trying str.replace...")
    html = html.replace('opacity:0', 'opacity: 1 !important')
    html = html.replace('transform:translateY(30px)', 'transform: none !important')
    print("Applied force replace")

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
