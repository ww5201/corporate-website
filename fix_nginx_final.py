import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. Remove tokai.conf (duplicate)
cmds = [
    'rm -f /etc/nginx/conf.d/tokai.conf',
    # 2. Rewrite site.conf - clean version without the shop/payment/login proxy rules
    """cat > /etc/nginx/conf.d/site.conf << 'EOF'
server {
    listen 80;
    server_name _;
    root /var/www/frontend;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /file-upload/ {
        proxy_pass http://127.0.0.1:9999/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF""",
    'nginx -t 2>&1',
    'nginx -s reload 2>&1',
    'sleep 1',
    # 3. Verify
    'echo "=== index.html ==="',
    'curl -sI http://localhost/ 2>/dev/null | head -5',
    'echo ""',
    'echo "=== shop.html ==="',
    'curl -sI http://localhost/shop.html 2>/dev/null | head -5',
    'echo ""',
    'echo "=== payment.html ==="',
    'curl -sI http://localhost/payment.html 2>/dev/null | head -5',
    'echo ""',
    'echo "=== API health ==="',
    'curl -s http://localhost/api/health 2>/dev/null',
    'echo ""',
    'echo "=== shop.html content check ==="',
    'curl -s http://localhost/shop.html 2>/dev/null | head -8',
    'echo ""',
    'echo "=== payment.html content check ==="',
    'curl -s http://localhost/payment.html 2>/dev/null | head -8',
    'echo ""',
    'echo "=== All files ==="',
    'ls -la /var/www/frontend/',
]
for cmd in cmds:
    i, o, e = ssh.exec_command(cmd, timeout=15)
    out = o.read().decode('utf-8', 'replace').strip()
    err = e.read().decode('utf-8', 'replace').strip()
    if out or err:
        print(f'>>> {cmd[:80]}')
        if out: print(out)
        if err and 'emerg' in err: print(f'ERR: {err}')
    print()

ssh.close()
print('Done!')
