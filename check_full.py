import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

cmds = [
    'ls -la /var/www/frontend/',
    'ls -la /var/www/frontend/assets/',
    'cat /var/www/frontend/index.html | head -5',
    'echo "---NGINX---"',
    'cat /etc/nginx/conf.d/*.conf 2>/dev/null',
    'echo "---NGINX SITES---"',
    'cat /etc/nginx/sites-enabled/* 2>/dev/null',
    'echo "---NGINX MAIN---"',
    'grep -r "root\\|server_name\\|location" /etc/nginx/nginx.conf 2>/dev/null | head -20',
    'echo "---PM2---"',
    'pm2 list 2>/dev/null',
    'echo "---SERVER CHECK---"',
    'curl -s http://localhost:3000/api/health 2>/dev/null',
    'echo ""',
    'curl -sI http://localhost/ 2>/dev/null | head -10',
    'echo "---SHOP CHECK---"',
    'ls -la /var/www/frontend/shop.html 2>/dev/null',
    'ls -la /root/backend/frontend/shop.html 2>/dev/null',
    'echo "---FIND SHOP---"',
    'find /var/www -name "shop.html" 2>/dev/null',
    'find /root -maxdepth 4 -name "shop.html" 2>/dev/null',
    'echo "---PAYMENT CHECK---"',
    'find /var/www -name "payment.html" 2>/dev/null',
    'find /root -maxdepth 4 -name "payment.html" 2>/dev/null',
]
for cmd in cmds:
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    err = e.read().decode('utf-8', 'replace').strip()
    if out:
        print(f'>>> {cmd}')
        print(out)
    if err and 'no such file' not in err.lower() and 'not found' not in err.lower():
        print(f'ERR: {err}')
    print()

ssh.close()
