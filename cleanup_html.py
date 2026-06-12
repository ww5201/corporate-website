import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
html = stdout.read().decode('utf-8')

print("Before cleanup:")
idx = html.find('<script>\nfunction callPhone')
if idx >= 0:
    print("  Found callPhone function at", idx)
    # Remove the extra <script> block that contains callPhone
    start = html.rfind('</script>', 0, idx)
    end = html.find('</script>', idx) + len('</script>')
    print("  Removing from", start, "to", end)
    if start >= 0:
        # Remove the entire second script block
        old_script = html[start:end]
        html = html.replace(old_script, '')
        print("  Removed extra callPhone script")

# Also make sure the tel: links work properly
# Change from: <a href="tel:18977122166" ... onclick="..."> to simple tel: link
old = '<a href="tel:18977122166" style="color:inherit;text-decoration:none" onclick="if(window.Android){Android.callPhone(\'18977122166\');return false;}">18977122166</a>'
new = '<a href="tel:18977122166" style="color:inherit;text-decoration:none">18977122166</a>'
if old in html:
    html = html.replace(old, new)
    print("  Cleaned up onclick from tel links")

print("Total tel: links:", html.count('tel:18977122166'))
print("callPhone refs:", html.count('callPhone'))

# Write back
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# Reload nginx
ssh.exec_command('nginx -s reload')

# Sync to local
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
