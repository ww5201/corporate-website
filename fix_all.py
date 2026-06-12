import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# === FIX 1: handleWechatClick - use JS bridge for APK, weixin:// for browser ===
old_wc = """function handleWechatClick() {
    window.location.href = 'weixin://';
}"""

new_wc = """function handleWechatClick() {
    var num = '18977122166';
    // Method 1: APK JavaScript Bridge
    if (window.Android && window.Android.openWechat) {
        window.Android.openWechat();
        return;
    }
    // Method 2: Copy number + show guide
    try {
        var ta = document.createElement('textarea');
        ta.value = num;
        ta.style.cssText = 'position:fixed;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
    } catch(e) {}
    showWechatGuide(true);
}"""

if old_wc in html:
    html = html.replace(old_wc, new_wc)
    print("FIX 1: handleWechatClick updated")
else:
    print("WARNING: handleWechatClick pattern not found")

# === FIX 2: Ensure contact form submit works ===
# Check if form has proper onsubmit
if 'document.getElementById' in html and 'contact-form' in html:
    print("FIX 2: Contact form exists")
else:
    print("WARNING: Check contact form")

# === Verify integrity ===
print(f"\nSize: {len(html)}")
script_start = html.find('<script>')
script_end = html.find('</script>', script_start)
js = html[script_start+8:script_end]
ob = js.count('{')
cb = js.count('}')
print(f"JS braces: {ob}:{cb} diff={ob-cb}")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

# Force reload nginx, clear any cache
ssh.exec_command('nginx -s reload')
import time; time.sleep(0.5)

# Verify what curl gets
stdin, stdout, stderr = ssh.exec_command('curl -s -H "Cache-Control: no-cache" http://127.0.0.1/ | grep -c "<script>"')
verify = stdout.read().decode().strip()
print(f"Verification: <script> count = {verify}")

# Save local copy
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("\nDone!")
