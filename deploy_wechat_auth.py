import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=15)

# 1. Backup current auth.js
stdin, stdout, stderr = ssh.exec_command('cp /root/backend/routes/auth.js /root/backend/routes/auth.js.bak')
stdout.channel.recv_exit_status()
print("[1] Backup done")

# 2. Read the new auth file from local
with open('D:\\tokai\\auth_new.js', 'r', encoding='utf-8') as f:
    new_content = f.read()

# 3. Upload via SFTP
sftp = ssh.open_sftp()
with sftp.file('/root/backend/routes/auth.js', 'w') as f:
    f.write(new_content)
sftp.close()
print("[2] Upload done, size:", len(new_content))

# 4. Set WeChat env vars
env_cmd = '''
export WECHAT_APP_ID="wx187d6ca3a6da9ca3"
export WECHAT_APP_SECRET="fbb6ed4e1276bf5141a0cf64393e0a23"
'''
# Write to .env file for persistence
env_file = 'WECHAT_APP_ID=wx187d6ca3a6da9ca3\nWECHAT_APP_SECRET=fbb6ed4e1276bf5141a0cf64393e0a23\nJWT_SECRET=luxury-co-secret-key-2026\n'
sftp2 = ssh.open_sftp()
with sftp2.file('/root/backend/.env', 'w') as f:
    f.write(env_file)
sftp2.close()
print("[3] .env file created")

# 5. Check if backend uses dotenv or process.env
stdin, stdout, stderr = ssh.exec_command('head -30 /root/backend/server-v4.js')
server_head = stdout.read().decode('utf-8', errors='replace')
print("[4] server-v4.js head:", server_head[:500])

# 6. Restart backend
stdin, stdout, stderr = ssh.exec_command('cd /root/backend && pm2 restart tokai-backend 2>&1 || pm2 start server-v4.js --name tokai-backend 2>&1')
output = stdout.read().decode('utf-8', errors='replace')
print("[5] PM2 restart:", output[:500])

ssh.close()
print("[DONE] Backend updated with real WeChat login")
