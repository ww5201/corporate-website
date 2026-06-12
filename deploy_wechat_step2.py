import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# 1. Restart backend with env vars
stdin, stdout, stderr = ssh.exec_command(
    'export WECHAT_APP_ID=wx187d6ca3a6da9ca3 && '
    'export WECHAT_APP_SECRET=fbb6ed4e1276bf5141a0cf64393e0a23 && '
    'cd /root/backend && pm2 restart tokai-backend 2>&1'
)
out = stdout.read().decode('utf-8', errors='replace')
print("[1] PM2 restart:", out[:800])

# 2. Check if dotenv is used in server-v4.js
stdin, stdout, stderr = ssh.exec_command('grep -n dotenv /root/backend/server-v4.js')
dotenv_check = stdout.read().decode('utf-8', errors='replace')
print("[2] dotenv check:", dotenv_check if dotenv_check else "NOT FOUND - need to add")

# 3. Verify the new auth.js is in place
stdin, stdout, stderr = ssh.exec_command('grep -n "sns/oauth2" /root/backend/routes/auth.js')
verify = stdout.read().decode('utf-8', errors='replace')
print("[3] Verify new auth:", verify if verify else "MISSING!")

# 4. Check backend status
stdin, stdout, stderr = ssh.exec_command('pm2 status 2>&1')
status = stdout.read().decode('utf-8', errors='replace')
print("[4] PM2 status:", status[:500])

ssh.close()
print("[DONE]")
