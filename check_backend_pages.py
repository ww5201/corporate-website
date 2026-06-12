import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

cmds = [
    'echo "=== shop.html head ==="',
    'head -20 /root/backend/shop.html',
    'echo ""',
    'echo "=== payment.html head ==="',
    'head -20 /root/backend/payment.html',
    'echo ""',
    'echo "=== curl shop.html via backend ==="',
    'curl -s http://localhost:3000/shop.html | head -15',
    'echo ""',
    'echo "=== curl payment.html via backend ==="',
    'curl -s http://localhost:3000/payment.html | head -15',
    'echo ""',
    'echo "=== check server-v4.js for shop/payment routes ==="',
    'grep -n "shop\\|payment\\|admin\\|html" /root/backend/server-v4.js',
    'echo ""',
    'echo "=== nginx reload ==="',
    'nginx -s reload 2>&1',
]
for cmd in cmds:
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    err = e.read().decode('utf-8', 'replace').strip()
    print(f'>>> {cmd}')
    if out: print(out)
    if err and 'no such' not in err.lower(): print(f'ERR: {err}')
    print()

ssh.close()
