import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# 1. Check if dotenv is installed
stdin, stdout, stderr = ssh.exec_command('cd /root/backend && ls node_modules/dotenv 2>&1 || echo "NOT_INSTALLED"')
check = stdout.read().decode('utf-8', errors='replace')
print("[1] dotenv module:", "INSTALLED" if "NOT_INSTALLED" not in check else "NOT INSTALLED")

# 2. If not installed, install it
if "NOT_INSTALLED" in check:
    stdin, stdout, stderr = ssh.exec_command('cd /root/backend && npm install dotenv 2>&1')
    out = stdout.read().decode('utf-8', errors='replace')
    print("[2] Installed dotenv:", out[-200:])
else:
    print("[2] dotenv already installed")

# 3. Add dotenv loading at top of server-v4.js if not there
stdin, stdout, stderr = ssh.exec_command('head -5 /root/backend/server-v4.js')
head = stdout.read().decode('utf-8', errors='replace')
print("[3] Current head:", head[:200])

if "dotenv" not in head:
    # Use sed to add require('dotenv').config() after first line
    ssh.exec_command(r"""sed -i '1s|^|require("dotenv").config();\n|' /root/backend/server-v4.js""")
    print("[3a] Added dotenv.config() to server-v4.js")

# 4. Verify
stdin, stdout, stderr = ssh.exec_command('head -5 /root/backend/server-v4.js')
verify = stdout.read().decode('utf-8', errors='replace')
print("[4] After edit:", verify[:200])

# 5. Restart with --update-env and env vars
stdin, stdout, stderr = ssh.exec_command(
    'export WECHAT_APP_ID=wx187d6ca3a6da9ca3 && '
    'export WECHAT_APP_SECRET=fbb6ed4e1276bf5141a0cf64393e0a23 && '
    'cd /root/backend && pm2 restart tokai-backend --update-env 2>&1'
)
out = stdout.read().decode('utf-8', errors='replace')
print("[5] PM2 restart --update-env:", out[:500])

# 6. Test the API
stdin, stdout, stderr = ssh.exec_command('curl -s -X POST http://localhost:3000/api/auth/wechat/login -H "Content-Type: application/json" -d \'{"code":"test_invalid_code"}\' 2>&1')
test = stdout.read().decode('utf-8', errors='replace')
print("[6] Test wechat/login:", test[:300])

ssh.close()
print("[DONE]")
