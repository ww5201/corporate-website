import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# 1. Check PM2 status
stdin, stdout, stderr = ssh.exec_command('pm2 status 2>&1')
pm2_status = stdout.read().decode('utf-8', errors='replace')
print("[1] PM2 Status:")
print(pm2_status[:800])

# 2. Check if backend is listening on port 3000
stdin, stdout, stderr = ssh.exec_command('ss -tlnp | grep 3000 2>&1')
port_check = stdout.read().decode('utf-8', errors='replace')
print("\n[2] Port 3000:", port_check.strip() if port_check.strip() else "NOT LISTENING")

# 3. Check backend logs for errors
stdin, stdout, stderr = ssh.exec_command('pm2 logs tokai-backend --lines 30 --nostream 2>&1')
logs = stdout.read().decode('utf-8', errors='replace')
print("\n[3] Backend Logs (last 30 lines):")
print(logs[-1500:])

# 4. Check server-v4.js head for syntax issues
stdin, stdout, stderr = ssh.exec_command('head -8 /root/backend/server-v4.js')
head = stdout.read().decode('utf-8', errors='replace')
print("\n[4] server-v4.js head:")
print(head)

# 5. Try to test if node can load server-v4.js
stdin, stdout, stderr = ssh.exec_command('cd /root/backend && node -e "require(\"./server-v4.js\")" 2>&1 | head -20')
test_load = stdout.read().decode('utf-8', errors='replace')
test_err = stderr.read().decode('utf-8', errors='replace')
print("\n[5] Load test stdout:", test_load[:500])
print("    Load test stderr:", test_err[:500])

ssh.close()
print("\n[DONE]")
