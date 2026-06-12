import paramiko, sys
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

cmds = [
    'echo "=== server chat.html ==="',
    'cat /var/www/chat.html 2>/dev/null || echo "NOT FOUND"',
    'echo "=== frontend chat.html ==="',
    'cat /var/www/frontend/chat.html 2>/dev/null || echo "NOT FOUND"',
    'echo "=== frontend src dir ==="',
    'ls -la /var/www/frontend/src/ 2>/dev/null || echo "NO SRC DIR"',
    'echo "=== src/chat.js ==="',
    'cat /var/www/frontend/src/chat.js 2>/dev/null || echo "NOT FOUND"',
    'echo "=== src/style.css (first 50 lines) ==="',
    'head -50 /var/www/frontend/src/style.css 2>/dev/null || echo "NOT FOUND"',
    'echo "=== nginx chat route ==="',
    'grep -n "chat" /etc/nginx/conf.d/site.conf 2>/dev/null || echo "no chat in nginx"',
    'echo "=== server-v4.js chat routes ==="',
    'grep -n "chat" /var/www/server-v4.js | head -20',
]

stdin, stdout, stderr = client.exec_command(' && '.join(cmds))
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
if out: print(out)
if err: print('STDERR:', err, file=sys.stderr)
client.close()
