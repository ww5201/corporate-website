import paramiko
import os
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()

BACKEND_LOCAL = r'D:\tokai\backend'
FRONTEND_LOCAL = r'D:\tokai\frontend'
REMOTE_BACKEND = '/root/backend'

def upload_file(local, remote):
    sftp.put(local, remote)
    print(f'  OK: {os.path.basename(local)} -> {remote}')

def ensure_remote_dir(remote_path):
    try:
        sftp.stat(remote_path)
    except FileNotFoundError:
        ensure_remote_dir(os.path.dirname(remote_path))
        sftp.mkdir(remote_path)

# 1. Upload server-v4.js
print('=== Backend Core ===')
upload_file(os.path.join(BACKEND_LOCAL, 'server-v4.js'), f'{REMOTE_BACKEND}/server-v4.js')

# 2. Upload routes
print('=== Routes ===')
for f in ['auth.js', 'payment.js']:
    local = os.path.join(BACKEND_LOCAL, 'routes', f)
    if os.path.exists(local):
        upload_file(local, f'{REMOTE_BACKEND}/routes/{f}')

# 3. Upload middleware
print('=== Middleware ===')
for f in os.listdir(os.path.join(BACKEND_LOCAL, 'middleware')):
    local = os.path.join(BACKEND_LOCAL, 'middleware', f)
    upload_file(local, f'{REMOTE_BACKEND}/middleware/{f}')

# 4. Upload models (keep for reference)
print('=== Models ===')
for f in os.listdir(os.path.join(BACKEND_LOCAL, 'models')):
    local = os.path.join(BACKEND_LOCAL, 'models', f)
    upload_file(local, f'{REMOTE_BACKEND}/models/{f}')

# 5. Upload admin.html
print('=== Admin ===')
admin_local = os.path.join(BACKEND_LOCAL, 'admin-v2.html')
if os.path.exists(admin_local):
    sftp.put(admin_local, f'{REMOTE_BACKEND}/admin.html')
    print('  OK: admin-v2.html -> admin.html')
elif os.path.exists(os.path.join(BACKEND_LOCAL, 'admin.html')):
    upload_file(os.path.join(BACKEND_LOCAL, 'admin.html'), f'{REMOTE_BACKEND}/admin.html')

# 6. Upload sms-service.js
sms_local = os.path.join(BACKEND_LOCAL, 'sms-service.js')
if os.path.exists(sms_local):
    upload_file(sms_local, f'{REMOTE_BACKEND}/sms-service.js')

# 7. Upload frontend SPA
print('=== Frontend SPA ===')
for root, dirs, files in os.walk(FRONTEND_LOCAL):
    # Skip node_modules and package files
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.git')]
    for f in files:
        if f in ('package.json', 'package-lock.json', 'vite.config.js'):
            continue
        local = os.path.join(root, f)
        rel = os.path.relpath(local, FRONTEND_LOCAL).replace('\\', '/')
        remote = f'{REMOTE_BACKEND}/frontend/{rel}'
        ensure_remote_dir(os.path.dirname(remote))
        sftp.put(local, remote)
        print(f'  {rel}')

sftp.close()

# 8. Install ws package
print('=== Installing ws package ===')
stdin, stdout, stderr = ssh.exec_command(f'cd {REMOTE_BACKEND} && npm install ws 2>&1 | tail -5', timeout=60)
print(stdout.read().decode('utf-8', 'replace').strip())

# 9. Restart backend with pm2
print('=== Restarting Backend ===')
stdin, stdout, stderr = ssh.exec_command(
    f'cd {REMOTE_BACKEND} && pm2 delete tokai-backend 2>/dev/null; pm2 start server-v4.js --name tokai-backend && pm2 save',
    timeout=15
)
out = stdout.read().decode('utf-8', 'replace')
err = stderr.read().decode('utf-8', 'replace')
print(out.strip() or err.strip())

# 10. Reload nginx
print('=== Reloading Nginx ===')
stdin, stdout, stderr = ssh.exec_command('systemctl reload nginx 2>&1', timeout=10)
print(stderr.read().decode('utf-8', 'replace').strip() or 'OK')

# 11. Health check
print('=== Health Check ===')
time.sleep(3)
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/health', timeout=10)
health = stdout.read().decode('utf-8', 'replace').strip()
print(f'  API: {health}')

stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/', timeout=10)
frontend_status = stdout.read().decode('utf-8', 'replace').strip()
print(f'  Frontend: HTTP {frontend_status}')

stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/api/products | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\'{len(d)} products\')" 2>&1', timeout=10)
products = stdout.read().decode('utf-8', 'replace').strip()
print(f'  Products: {products}')

# 12. Verify frontend serves SPA
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:3000/ | head -5', timeout=10)
html = stdout.read().decode('utf-8', 'replace').strip()
print(f'  HTML: {html[:100]}...')

ssh.close()
print('\n=== Deployed! ===')
