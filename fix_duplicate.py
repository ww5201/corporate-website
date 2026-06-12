import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# File structure: [DOCTYPE+html1][duplicate html2]
# First <head> at 38, second <head> at 75001
# Keep only from 0 to before second <head>
second_head = html.find('<head>', 50)  # skip first one
print(f"Second <head> at: {second_head}")

# Extract clean first copy - go to first </html> or end of first body section
# The first copy ends where the second copy begins
clean = html[:second_head]

# Make sure it ends properly
if not clean.rstrip().endswith('</html>'):
    # Find where the first copy's content ends
    last_body_close = clean.rfind('</body>')
    if last_body_close > 0:
        # Check if </html> follows
        rest = clean[last_body_close:last_body_close+20]
        print(f"End context: {repr(rest)}")
        if '</html>' in clean[last_body_close:]:
            html_end = clean.find('</html>', last_body_close)
            clean = clean[:html_end+7]

# Verify structure
print(f"Clean size: {len(clean)} chars")
print(f"<!DOCTYPE: {'<!DOCTYPE' in clean}")
print(f"</html>: {clean.count('</html>')}")
print(f"<head>: {clean.count('<head>')}")
print(f"<body>: {clean.count('<body>')}")

# Check if .reveal fix is present
print(f".reveal fixed: {'opacity: 1 !important' in clean}")
print(f"weixin://: {'weixin://' in clean}")

# Write clean version
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(clean)
sftp.close()

ssh.exec_command('nginx -s reload')

# Save local backup
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(clean)

ssh.close()
print("Done!")
