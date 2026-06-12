import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

# Find mobile-nav section
mn_start = html.find('class="mobile-nav"')
if mn_start >= 0:
    # Go back to opening tag
    tag_start = html.rfind('<', 0, mn_start)
    # Find closing tag
    tag_end = html.find('</div>', mn_start + 100)
    while tag_end > 0 and html[tag_end-1:tag_end+6] != '</div>':
        tag_end = html.find('</div>', tag_end + 1)
    tag_end += 6
    mobile_nav = html[tag_start:tag_end]
else:
    mobile_nav = "NOT FOUND"

with open('D:/tokai/mobile_nav_now.txt', 'w', encoding='utf-8') as f:
    f.write(mobile_nav)

print(f"Mobile nav: {len(mobile_nav)} chars")
ssh.close()
