import paramiko, sys
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

cmds = [
    'echo "=== find server-v4.js ==="',
    'find / -name "server-v4.js" -type f 2>/dev/null | head -5',
    'echo "=== find chat.html ==="',
    'find / -name "chat.html" -type f 2>/dev/null | head -5',
    'echo "=== PM2 process ==="',
    'pm2 jlist 2>/dev/null | python3 -c "import sys,json;data=json.load(sys.stdin);[print(p[\"name\"],p.get(\"pm2_env\",{}).get(\"pm_exec_path\",\"?\"),p.get(\"pm2_env\",{}).get(\"pm_cwd\",\"?\")) for p in data]" 2>/dev/null || pm2 list',
    'echo "=== nginx full config ==="',
    'cat /etc/nginx/conf.d/site.conf 2>/dev/null; echo "---"; cat /etc/nginx/sites-enabled/* 2>/dev/null; echo "---"; cat /etc/nginx/nginx.conf 2>/dev/null | head -40',
    'echo "=== frontend dir ==="',
    'ls -la /var/www/frontend/ 2>/dev/null || echo "no frontend dir"',
    'echo "=== var www structure ==="',
    'ls -la /var/www/ 2>/dev/null',
]

stdin, stdout, stderr = client.exec_command(' && '.join(cmds))
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
if out: print(out)
if err: print('STDERR:', err)
client.close()
