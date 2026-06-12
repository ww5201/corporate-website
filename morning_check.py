import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. Check server file
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# 2. Check backend
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/health')
health = stdout.read().decode()

# 3. Validate JS with Node
val_cmd = '''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);
try {
    new Function(js);
    console.log('JS OK, len=' + js.length + ', funcs=' + (js.match(/function \\w+/g) || []).length);
} catch(e) {
    console.log('JS ERROR: ' + e.message);
}
"'''
stdin, stdout, stderr = ssh.exec_command(val_cmd)
js_result = stdout.read().decode()

# 4. Check recent nginx access log
stdin, stdout, stderr = ssh.exec_command('tail -5 /var/log/nginx/access.log')
recent_log = stdout.read().decode()

with open('D:/tokai/morning_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {len(html)}\n")
    f.write(f"Has selectPay: {'function selectPay' in html}\n")
    f.write(f"Has handleWechatClick: {'function handleWechatClick' in html}\n")
    f.write(f"Has Android bridge: {'window.Android' in html}\n")
    f.write(f"Health: {health}\n")
    f.write(f"JS: {js_result}\n")
    f.write(f"Recent log:\n{recent_log}\n")

ssh.close()
print("Done")
