import paramiko, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

# Step 1: Check current nginx config
print("=== Current nginx site.conf ===")
stdin, stdout, stderr = client.exec_command('cat /etc/nginx/conf.d/site.conf 2>/dev/null || cat /etc/nginx/conf.d/tokai.conf 2>/dev/null')
current_config = stdout.read().decode('utf-8', errors='replace')
print(current_config)

# Step 2: Find which config file nginx is using
print("=== Nginx conf.d files ===")
stdin, stdout, stderr = client.exec_command('ls -la /etc/nginx/conf.d/')
print(stdout.read().decode('utf-8', errors='replace'))

# Step 3: Use site.conf specifically (where location / is defined)
config_file = '/etc/nginx/conf.d/site.conf'

if not config_file:
    print("ERROR: No nginx config file found!")
    client.close()
    sys.exit(1)

print(f"Editing config: {config_file}")

# Step 4: Add admin and chat proxy locations
fix_cmd = f"""python3 << 'PYEOF'
with open('{config_file}', 'r') as f:
    c = f.read()

print('Current config:')
print(c)
print('---')

changed = False

# Add admin location if not present
if 'location /admin' not in c:
    admin_block = '''
    location /admin {{
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
    }}

    location /admin.html {{
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
    }}

'''
    # Replace 'location / {{' (the catch-all) with admin blocks + catch-all
    old_str = '    location / {{'
    new_str = admin_block + '    location / {{'
    if old_str in c:
        c = c.replace(old_str, new_str)
        changed = True
        print('Added admin routes')
    else:
        print('WARNING: Could not find location / block to insert before')
else:
    print('Admin routes already exist')

if changed:
    with open('{config_file}', 'w') as f:
        f.write(c)
    print('Config updated')
else:
    print('No changes needed')
PYEOF
"""

print("\n=== Applying fix ===")
stdin, stdout, stderr = client.exec_command(fix_cmd)
print(stdout.read().decode('utf-8', errors='replace'))
err = stderr.read().decode('utf-8', errors='replace')
if err: print('STDERR:', err)

# Step 5: Test nginx config
print("\n=== Testing nginx ===")
stdin, stdout, stderr = client.exec_command('nginx -t 2>&1')
test_result = stdout.read().decode('utf-8', errors='replace')
print(test_result)

if 'successful' in test_result.lower() or 'ok' in test_result.lower():
    # Step 6: Reload nginx
    print("=== Reloading nginx ===")
    stdin, stdout, stderr = client.exec_command('systemctl reload nginx && echo RELOAD OK')
    print(stdout.read().decode('utf-8', errors='replace').strip())
    time.sleep(2)
    
    # Step 7: Copy admin.html to frontend as static backup
    print("\n=== Copy admin.html to frontend ===")
    stdin, stdout, stderr = client.exec_command('cp /root/backend/admin.html /var/www/frontend/admin.html && echo COPIED')
    print(stdout.read().decode('utf-8', errors='replace').strip())
    
    # Step 8: Verify
    print("\n=== Verification ===")
    tests = [
        ('chat.html', 'curl -s -o /dev/null -w "%{http_code}" http://8.138.218.146/chat.html'),
        ('admin', 'curl -s -o /dev/null -w "%{http_code}" http://8.138.218.146/admin'),
        ('admin.html', 'curl -s -o /dev/null -w "%{http_code}" http://8.138.218.146/admin.html'),
        ('api/conversations', 'curl -s -o /dev/null -w "%{http_code}" http://8.138.218.146/api/conversations'),
        ('index', 'curl -s -o /dev/null -w "%{http_code}" http://8.138.218.146/'),
    ]
    for name, cmd in tests:
        stdin, stdout, stderr = client.exec_command(cmd + ' && echo')
        status = stdout.read().decode('utf-8', errors='replace').strip()
        print(f'  {name}: {status}')
else:
    print("nginx config test failed, NOT reloading!")
    print("Showing updated config for debugging:")
    stdin, stdout, stderr = client.exec_command(f'cat {config_file}')
    print(stdout.read().decode('utf-8', errors='replace'))

client.close()
print("\nDone!")
