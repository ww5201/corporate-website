import paramiko, sys, os, base64

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

HOST = '8.138.218.146'
USER = 'root'
PWD = 'ww0987654.'

# Read local chat.html
with open('D:/tokai/chat.html', 'r', encoding='utf-8') as f:
    chat_html = f.read()

# Base64 encode for safe transfer
b64 = base64.b64encode(chat_html.encode('utf-8')).decode('ascii')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USER, PWD, timeout=10)

print("=" * 60)
print("DEPLOYING chat.html")
print("=" * 60)

# Step 1: Upload chat.html
print("\n=== Upload chat.html to /var/www/frontend/ ===")
cmd = f'echo "{b64}" | base64 -d > /var/www/frontend/chat.html && wc -c /var/www/frontend/chat.html'
stdin, stdout, stderr = client.exec_command(cmd)
print(stdout.read().decode('utf-8', errors='replace').strip())
err = stderr.read().decode('utf-8', errors='replace').strip()
if err: print("ERR:", err)

# Step 2: Verify file exists
print("\n=== Verify file ===")
stdin, stdout, stderr = client.exec_command('ls -la /var/www/frontend/chat.html')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Step 3: Add chat.html route to server-v4.js (for backend fallback)
print("\n=== Check if server-v4.js has chat route ===")
stdin, stdout, stderr = client.exec_command('grep -n "chat.html" /root/backend/server-v4.js')
out = stdout.read().decode('utf-8', errors='replace').strip()
if out:
    print("Already has chat route:", out)
else:
    print("Adding chat.html route to server-v4.js...")
    # Find the shop.html route line and add chat.html route before it
    add_route = r'''python3 -c "
import re
with open('/root/backend/server-v4.js','r') as f: c=f.read()
if '/chat.html' not in c:
    c = c.replace(
        'app.get(\"/shop.html\"',
        'app.get(\"/chat.html\", (req, res) => { const p = require(\"path\").join(__dirname, \"chat.html\"); if (require(\"fs\").existsSync(p)) return res.sendFile(p); res.sendFile(require(\"path\").join(__dirname, \"frontend\", \"index.html\")); });\napp.get(\"/shop.html\"'
    )
    with open('/root/backend/server-v4.js','w') as f: f.write(c)
    print('chat.html route added')
else:
    print('chat.html route already exists')
"'''
    stdin, stdout, stderr = client.exec_command(add_route)
    print(stdout.read().decode('utf-8', errors='replace').strip())
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if err: print("ERR:", err)

# Step 4: Restart backend
print("\n=== Restart backend ===")
stdin, stdout, stderr = client.exec_command('pm2 restart tokai-backend')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Step 5: Wait and verify
import time
time.sleep(2)

print("\n=== Verify chat.html via curl ===")
stdin, stdout, stderr = client.exec_command('curl -sI http://localhost/chat.html')
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Verify chat.html content (first 5 lines) ===")
stdin, stdout, stderr = client.exec_command('curl -s http://localhost/chat.html | head -5')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Step 6: Test conversation API
print("\n=== Test conversation API ===")
stdin, stdout, stderr = client.exec_command('''curl -s -X POST http://localhost:3000/api/conversations -H "Content-Type: application/json" -d '{"visitorId":"test_deploy","name":"test","phone":""}' ''')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Step 7: Verify WebSocket path
print("\n=== Test WebSocket path ===")
stdin, stdout, stderr = client.exec_command('curl -sI -H "Upgrade: websocket" -H "Connection: Upgrade" http://localhost/ws/chat?convId=test 2>&1 | head -3')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Step 8: Check all frontend files
print("\n=== Final frontend files ===")
stdin, stdout, stderr = client.exec_command('ls -la /var/www/frontend/')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Step 9: Add navigation link in index.html if not present
print("\n=== Check if index.html has chat link ===")
stdin, stdout, stderr = client.exec_command('grep -n "chat.html" /var/www/frontend/index.html')
out = stdout.read().decode('utf-8', errors='replace').strip()
if out:
    print("Already has chat link:", out)
else:
    print("Adding chat link to index.html navigation...")
    # Add a chat link in the nav after the payment link
    add_nav = r'''python3 -c "
with open('/var/www/frontend/index.html','r') as f: c=f.read()
if 'chat.html' not in c:
    # Add to desktop nav
    c = c.replace(
        '<li><a href=\"/payment.html\" target=\"_blank\">在线支付</a></li>',
        '<li><a href=\"/payment.html\" target=\"_blank\">在线支付</a></li>\n        <li><a href=\"/chat.html\" target=\"_blank\">在线咨询</a></li>'
    )
    # Add to mobile nav
    c = c.replace(
        '<a href=\"/payment.html\" target=\"_blank\">在线支付</a>',
        '<a href=\"/payment.html\" target=\"_blank\">在线支付</a>\n      <a href=\"/chat.html\" target=\"_blank\">在线咨询</a>'
    )
    with open('/var/www/frontend/index.html','w') as f: f.write(c)
    print('chat link added to index.html')
else:
    print('chat link already exists')
"'''
    stdin, stdout, stderr = client.exec_command(add_nav)
    print(stdout.read().decode('utf-8', errors='replace').strip())
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if err: print("ERR:", err)

print("\n" + "=" * 60)
print("DEPLOY COMPLETE!")
print("=" * 60)

client.close()
