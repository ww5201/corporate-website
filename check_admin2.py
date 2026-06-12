import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

# Fix the escaped dollar signs in admin blocks
# Read current config
stdin, stdout, stderr = client.exec_command('cat /etc/nginx/conf.d/site.conf')
config = stdout.read().decode('utf-8', errors='replace')

# Fix: replace \$ with $ in the admin blocks
fixed_config = config.replace('\\$', '$')
print("=== Fixed config ===")
print(fixed_config)

# Write fixed config back using SFTP
sftp = client.open_sftp()
with sftp.open('/etc/nginx/conf.d/site.conf', 'w') as f:
    f.write(fixed_config)
sftp.close()
print("\nConfig written!")

# Test nginx config
stdin, stdout, stderr = client.exec_command('nginx -t 2>&1')
test = stdout.read().decode('utf-8', errors='replace')
print("\n=== nginx test ===")
print(test)

if 'successful' in test.lower():
    # Reload
    stdin, stdout, stderr = client.exec_command('systemctl reload nginx')
    print("Reload:", stdout.read().decode('utf-8', errors='replace').strip(), stderr.read().decode('utf-8', errors='replace').strip())
    time.sleep(1)
    
    # Test all endpoints
    print("\n=== Final tests ===")
    tests = [
        ('admin page', 'curl -s http://localhost/admin | head -3'),
        ('admin.html', 'curl -s -o /dev/null -w "%{http_code}" http://localhost/admin.html && echo'),
        ('api/products', 'curl -s http://localhost/api/products | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d),\'products\')"'),
        ('api/messages', 'curl -s http://localhost/api/messages | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d),\'messages\')"'),
        ('api/orders', 'curl -s http://localhost/api/orders | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d),\'orders\')"'),
        ('api/conversations', 'curl -s http://localhost/api/conversations | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d),\'conversations\')"'),
        ('chat.html', 'curl -s -o /dev/null -w "%{http_code}" http://localhost/chat.html && echo'),
    ]
    for name, cmd in tests:
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='replace').strip()
        print(f'  {name}: {out}')
else:
    print("nginx test failed!")

client.close()
