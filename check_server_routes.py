import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Get the full server-v4.js static/routing section
cmds = [
    'echo "=== server-v4.js static & routing section ==="',
    'sed -n "460,490p" /root/backend/server-v4.js',
    'echo ""',
    'echo "=== server-v4.js shop/payment routes ==="',
    'grep -n "shop\\|payment\\|login\\|\.html" /root/backend/server-v4.js',
    'echo ""',
    'echo "=== admin.html exists? ==="',
    'ls -la /root/backend/admin.html 2>/dev/null',
    'echo ""',
    'echo "=== Check if backend serves shop.html directly ==="',
    'curl -sI http://localhost:3000/shop.html 2>/dev/null | head -5',
    'echo ""',
    'echo "=== Check if backend serves payment.html directly ==="',
    'curl -sI http://localhost:3000/payment.html 2>/dev/null | head -5',
    'echo ""',
    'echo "=== Check original dist/index.html on remote ==="',
    'head -5 /root/backend/dist/index.html',
]
for cmd in cmds:
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    print(f'>>> {cmd}')
    if out: print(out)
    print()

ssh.close()
