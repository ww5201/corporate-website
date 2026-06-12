import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()

# 1. Upload original index.html to /var/www/frontend/
sftp.put(r'D:\tokai\dist\index.html', '/var/www/frontend/index.html')
print('OK: index.html -> /var/www/frontend/index.html')

# 2. Create assets dir and copy old assets
cmds = [
    'mkdir -p /var/www/frontend/assets',
    'cp /root/backend/dist/assets/index-CVahQ6Nl.js /var/www/frontend/assets/',
    'cp /root/backend/dist/assets/index-BgVLAb6w.css /var/www/frontend/assets/',
    'rm -f /var/www/frontend/assets/index-CsYGjifK.js /var/www/frontend/assets/index-DfFAHtO8.css',
    'ls -la /var/www/frontend/',
    'ls -la /var/www/frontend/assets/',
]
for cmd in cmds:
    print(f'>>> {cmd}')
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    err = e.read().decode('utf-8', 'replace').strip()
    if out: print(out)
    if err and 'no such file' not in err.lower(): print(f'ERR: {err}')
    print()

# 3. Restart backend
print('>>> pm2 restart tokai-backend')
i, o, e = ssh.exec_command('pm2 restart tokai-backend', timeout=15)
out = o.read().decode('utf-8', 'replace').strip()
print(out)

sftp.close()
ssh.close()
print('\nDone! Original site restored.')
