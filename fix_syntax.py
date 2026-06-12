import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Fix the extra } after handleWechatClick
# Current broken:
# function handleWechatClick() {
#     window.location.href = 'weixin://';
# }
#     }
# Should be:
# function handleWechatClick() {
#     window.location.href = 'weixin://';
# }

old = """function handleWechatClick() {
    window.location.href = 'weixin://';
}
    }"""

new = """function handleWechatClick() {
    window.location.href = 'weixin://';
}"""

if old in html:
    html = html.replace(old, new)
    print("Fixed extra }")
else:
    print("Pattern not found, checking...")
    idx = html.find('function handleWechatClick')
    if idx >= 0:
        print(f"At {idx}: {repr(html[idx:idx+150])}")

# Verify
print(f"\nSize: {len(html)} chars")
print(f"loadData() calls: {html.count('loadData()')}")
print(f"renderProducts: {'function renderProducts' in html}")

# Check JS syntax - count braces in script
script_start = html.find('<script>', html.find('<head>'))
script_end = html.find('</script>', script_start)
js = html[script_start:script_end]
open_b = js.count('{')
close_b = js.count('}')
print(f"JS braces: open={open_b}, close={close_b}, diff={open_b-close_b}")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()
ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
