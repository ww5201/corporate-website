import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('cat /var/www/frontend/index.html')
html = stdout.read().decode('utf-8')

for kw in ['#footer', 'id="footer"', '<footer', 'footer-content', 'ICP', 'copyright', 'bot-nav', '卓翌定制']:
    idx = html.find(kw)
    status = "found at " + str(idx) if idx >= 0 else "NOT FOUND"
    print(kw + ": " + status)

print()
print("Last 300 chars:")
print(repr(html[-300:]))

# Check for the remaining callPhone function
if 'callPhone' in html:
    idx = html.find('callPhone')
    print("\ncallPhone found at " + str(idx))
    print(html[idx:idx+200])

count = html.count('</script>')
print("\nClosing script tags: " + str(count))

ssh.close()
