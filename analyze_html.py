import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"File size: {len(html)} chars")
print(f"<!DOCTYPE count: {html.count('<!DOCTYPE')}")
print(f"</html> count: {html.count('</html>')}")
print(f"<body> count: {html.count('<body>')}")
print(f"</body> count: {html.count('</body>')}")

# Find positions of key markers
for marker in ['<!DOCTYPE', '</html>', '<head>', '</head>', '<body>', '</body>']:
    positions = []
    start = 0
    while True:
        idx = html.find(marker, start)
        if idx < 0:
            break
        positions.append(idx)
        start = idx + 1
    print(f"{marker}: {positions}")

# Check for duplicate content pattern
first_end = html.find('</html>')
if first_end >= 0:
    after_first = html[first_end:first_end+50]
    print(f"\nFirst </html> context: {repr(after_first)}")

ssh.close()
