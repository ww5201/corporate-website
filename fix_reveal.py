import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
html = stdout.read().decode('utf-8')

# Fix: make .reveal elements visible by default
# Find the .reveal CSS rule and change opacity from 0 to 1
old_css = '.reveal { opacity: 0; transform: translateY(30px); transition: all 0.6s ease-out; }'
new_css = '.reveal { opacity: 1 !important; transform: none; }'

if old_css in html:
    html = html.replace(old_css, new_css)
    print("Fixed .reveal CSS: opacity 0 -> 1")
else:
    # Try alternative patterns
    if '.reveal' in html:
        idx = html.find('.reveal')
        print("Found .reveal at", idx)
        print(html[idx:idx+100])
    else:
        print(".reveal class not found in CSS")

# Also fix .visible rule if it exists
old_vis = '.reveal.visible { opacity: 1; transform: translateY(0); }'
if old_vis in html:
    html = html.replace(old_vis, '')
    print("Removed .visible override")

print(f"Total size: {len(html)} chars")

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
