import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

cmds = [
    # Check admin.html tabs/sections
    'echo "=== admin.html tab buttons ==="',
    'grep -n "tab\\|button.*管理\\|button.*留言\\|button.*咨询\\|button.*聊天\\|onclick.*show" /root/backend/admin.html',
    
    # Check if there's a conversations/chat section
    'echo ""',
    'echo "=== admin.html conversation/chat related ==="',
    'grep -n -i "conversation\\|chat\\|ws/\\|websocket\\|socket" /root/backend/admin.html',
    
    # Check the tab switching function
    'echo ""',
    'echo "=== admin.html showTab function ==="',
    'grep -A 20 "function show" /root/backend/admin.html | head -30',
    
    # Check all section divs
    'echo ""',
    'echo "=== admin.html section divs ==="',
    'grep -n "sec-\\|section\\|id=\\"" /root/backend/admin.html | grep -i "sec\\|panel\\|tab"',
    
    # Check server-v4.js conversation API endpoints
    'echo ""',
    'echo "=== server-v4.js conversation routes ==="',
    'grep -n "conversation\\|/ws/" /root/backend/server-v4.js | head -20',
    
    # Check chat.html for how visitor chat works
    'echo ""',
    'echo "=== chat.html structure (first 30 lines) ==="',
    'head -30 /var/www/frontend/chat.html 2>/dev/null || head -30 /root/backend/chat.html 2>/dev/null',
    
    # Full admin.html
    'echo ""',
    'echo "=== FULL admin.html ==="',
    'cat /root/backend/admin.html',
]

stdin, stdout, stderr = client.exec_command(' && '.join(cmds))
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out[:15000])
if err: print('STDERR:', err[:2000])
client.close()
