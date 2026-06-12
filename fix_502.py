import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# Fix: Change module.exports from object to router (backward compatible)
# Old: module.exports = { router, authMiddleware, adminMiddleware };
# New: module.exports = router; + attach middleware as properties

fix_cmd = r"""sed -i 's/module\.exports = { router, authMiddleware, adminMiddleware };/module.exports = router;\nrouter.authMiddleware = authMiddleware;\nrouter.adminMiddleware = adminMiddleware;/' /root/backend/routes/auth.js"""

stdin, stdout, stderr = ssh.exec_command(f'bash -c "{fix_cmd}"')
stdout.channel.recv_exit_status()

# Verify the fix
stdin, stdout, stderr = ssh.exec_command('tail -8 /root/backend/routes/auth.js')
tail = stdout.read().decode('utf-8', errors='replace')
print("[1] Fixed tail of auth.js:")
print(tail)

# Restart backend
stdin, stdout, stderr = ssh.exec_command('cd /root/backend && pm2 restart tokai-backend --update-env 2>&1')
restart = stdout.read().decode('utf-8', errors='replace')
print("\n[2] PM2 restart:", restart[:500])

import time; time.sleep(3)

# Check status
stdin, stdout, stderr = ssh.exec_command('pm2 status 2>&1')
status = stdout.read().decode('utf-8', errors='replace')
print("\n[3] PM2 Status:")
print(status[:400])

# Test API
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/auth/me 2>&1')
code = stdout.read().decode('utf-8', errors='replace')
print(f"\n[4] API test /api/auth/me => HTTP {code}")

ssh.close()
print("\n[DONE]")
