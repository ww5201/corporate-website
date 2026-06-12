import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

cmds = [
    'echo "=== admin.html API calls ==="',
    'grep -n "fetch" /root/backend/admin.html | head -20',
    'echo "=== admin.html admin API routes ==="',
    'grep -n "api/admin" /root/backend/admin.html | head -20',
    'echo "=== admin.html all API URLs ==="',
    'grep -oP "/api/[a-zA-Z0-9/_-]+" /root/backend/admin.html | sort -u',
    'echo "=== server-v4.js admin routes ==="',
    'grep -n "admin" /root/backend/server-v4.js | head -20',
    'echo "=== Test admin API endpoints ==="',
    'curl -s http://localhost:3000/api/admin/products 2>&1 | head -3',
    'echo ""',
    'curl -s http://localhost:3000/api/admin/messages 2>&1 | head -3',
    'echo ""',
    'curl -s http://localhost:3000/api/admin/orders 2>&1 | head -3',
    'echo ""',
    'curl -s http://localhost:3000/api/products 2>&1 | head -3',
    'echo ""',
    'curl -s http://localhost:3000/api/messages 2>&1 | head -3',
    'echo ""',
    'curl -s http://localhost:3000/api/orders 2>&1 | head -3',
    'echo ""',
    'echo "=== All API routes in server ==="',
    'grep -oP "/api/[a-zA-Z0-9/_:-]+" /root/backend/server-v4.js | sort -u',
]

stdin, stdout, stderr = client.exec_command(' && '.join(cmds))
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out)
if err: print('STDERR:', err)
client.close()
