import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

cmds = [
    'cat /root/backend/server-v4.js | grep -i "static\\|frontend\\|dist\\|public\\|express.static" | head -20',
    'pm2 list 2>/dev/null || systemctl status backend 2>/dev/null | head -10',
    'ls -la /root/backend/dist/',
    'ls -la /root/backend/dist/assets/ 2>/dev/null',
    'cat /etc/nginx/sites-enabled/* 2>/dev/null | head -30',
    'cat /etc/nginx/conf.d/* 2>/dev/null | head -30',
    'nginx -t 2>&1; cat /etc/nginx/nginx.conf 2>/dev/null | grep -A5 "server\\|root\\|proxy_pass" | head -30',
]
for cmd in cmds:
    print(f'>>> {cmd}')
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    err = e.read().decode('utf-8', 'replace').strip()
    if out: print(out)
    if err and 'warning' not in err.lower(): print(f'ERR: {err}')
    print()

ssh.close()
