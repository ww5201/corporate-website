import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

checks = [
    ('curl -s http://127.0.0.1:3000/api/health', 'Backend health'),
    ('curl -s http://127.0.0.1:3000/api/app-version', 'App version'),
    ("grep -c 'oName' /var/www/frontend/index.html", 'oName refs'),
    ("grep -c 'orderTitle' /var/www/frontend/index.html", 'orderTitle refs (should be 0)'),
    ("grep -c 'checkAppUpdate' /var/www/frontend/index.html", 'checkAppUpdate refs'),
    ("grep -c 'settings-menu' /var/www/frontend/index.html", 'settings-menu refs'),
]

with open('D:/tokai/verify_fix.txt', 'w', encoding='utf-8') as f:
    for cmd, label in checks:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode().strip()
        f.write(f"{label}: {result}\n")

ssh.close()

with open('D:/tokai/verify_fix.txt') as f:
    print(f.read())
