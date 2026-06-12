import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Step 1: Restore clean local backup
with open(r'D:/tokai/index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Local backup size: {len(html)} chars")

# Upload clean version
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()
print("Restored clean version to server")

# Step 2: Now make precise WeChat button change
# Find handleWechatClick function and replace it
stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
html2 = stdout.read().decode('utf-8')

# Use Python str.replace for exact string matching
# Find the double-click pattern and replace with single-click weixin:// jump

# Pattern 1: The full function replacement
old_func_start = 'function handleWechatClick() {\n    if (!wechatClickTime) {\n        wechatClickTime = Date.now();'
new_func = '''function handleWechatClick() {
    var wechatNum = '18977122166';
    
    // Try opening WeChat directly
    try {
        window.location.href = 'weixin://dl/business/?t=' + wechatNum;
        setTimeout(function() {
            showWechatGuide(false);
        }, 1500);
        return;
    } catch(e) {}
    
    // Fallback: show guide
    showWechatGuide(false);'''

if old_func_start in html2:
    html2 = html2.replace(old_func_start, new_func, 1)
    print("Replaced handleWechatClick function")
else:
    print("Pattern 1 not found")
    # Try finding just the start
    idx = html2.find('function handleWechatClick')
    if idx >= 0:
        print(f"Function at {idx}: {repr(html2[idx:idx+80])}")

# Also change button color back to WeChat green
old_color = 'background:#4caf50'
if old_color in html2:
    html2 = html2.replace(old_color, 'background:#07c160', 1)
    print("Changed button to WeChat green")

print(f"New size: {len(html2)} chars")
print(f"has weixin://: {'weixin://' in html2}")

# Write final version
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html2)
sftp.close()

ssh.exec_command('nginx -s reload')

# Sync local copy
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html2)

ssh.close()
print("Done!")
