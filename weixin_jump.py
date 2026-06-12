import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
html = stdout.read().decode('utf-8')

# Find current WeChat button handler and replace with weixin:// link approach
# Current: double-click -> showWechatGuide overlay
# New: single click -> try weixin:// protocol, fallback to guide

old_handler = '''function handleWechatClick() {
    if (!wechatClickTime) {
        wechatClickTime = Date.now();
        var btn = document.getElementById('wechatBtn');
        btn.style.backgroundColor = '#ff6b35';
        btn.innerHTML = '&#10003;';
        setTimeout(function() {
            btn.style.backgroundColor = '';
            btn.innerHTML = '&#128172;';
            wechatClickTime = 0;
        }, 2000);
        return;
    }
    if (Date.now() - wechatClickTime < 2000) {
        wechatClickTime = 0;
        var clipOk = false;'''

new_handler = '''function handleWechatClick() {
    // Try to open WeChat directly via weixin:// protocol
    var wechatNum = '18977122166';
    
    // Method 1: Try weixin:// URL scheme
    try {
        window.location.href = 'weixin://dl/business/?t=' + wechatNum;
        // If we're still here after 1.5s, WeChat probably didn't open
        setTimeout(function() {
            showWechatGuide(false);
        }, 1500);
        return;
    } catch(e) {
        // Fall through to guide
    }
    
    // Fallback: show guide with number
    showWechatGuide(false);'''

if old_handler in html:
    html = html.replace(old_handler, new_handler)
    print("Updated handleWechatClick to use weixin:// protocol")
else:
    print("Pattern not found exactly, trying partial match...")
    # Find and replace the function
    start = html.find('function handleWechatClick()')
    if start >= 0:
        end = html.find('\n}', html.find('// Fallback', start)) + 3
        old_func = html[start:end]
        print(f"Found function at {start}-{end}, length={len(old_func)}")
        html = html[:start] + new_handler + html[end:]
        print("Replaced function")

# Also reset the button appearance - remove double-click visual feedback
# Change button back to simple click style
old_btn_style = 'cursor:pointer;border-radius:50%;width:56px;height:56px;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 4px 15px rgba(0,0,0,0.2);transition:all 0.3s ease;z-index:998;background:#4caf50;color:#fff'
new_btn_style = 'cursor:pointer;border-radius:50%;width:56px;height:56px;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 4px 15px rgba(0,0,0,0.2);transition:all 0.3s ease;z-index:998;background:#07c160;color:#fff'

if old_btn_style in html:
    html = html.replace(old_btn_style, new_btn_style)
    print("Updated WeChat button color to WeChat green #07c160")

print(f"Total size: {len(html)} chars")
print(f"has weixin://: {'weixin://' in html}")

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
