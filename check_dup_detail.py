import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Extract JS
script_start = html.find('<script>') + 8
script_end = html.rfind('</script>')
js = html[script_start:script_end]

# Find the duplicate renderPortfolio
import re
# Find all renderPortfolio function positions
pattern = r'function renderPortfolio'
positions = [m.start() for m in re.finditer(pattern, js)]

with open('D:/tokai/dup_detail.txt', 'w', encoding='utf-8') as out:
    out.write(f"renderPortfolio positions: {positions}\n\n")
    for i, pos in enumerate(positions):
        context = js[pos:pos+500]
        out.write(f"--- renderPortfolio #{i+1} at {pos} ---\n{context}\n\n")

ssh.close()
print("Done")
