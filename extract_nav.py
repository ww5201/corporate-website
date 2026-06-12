import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find nav end to see structure
nav_start = html.find('<nav class="nav"')
nav_end = html.find('</nav>', nav_start) + 6
nav_section = html[nav_start:nav_end]

# Write to file
with open('D:/tokai/nav_section.txt', 'w', encoding='utf-8') as f:
    f.write(nav_section)

print(f"Nav section: {len(nav_section)} chars")
print("Written to D:/tokai/nav_section.txt")

# Find settings dropdown
dd_start = html.find('id="settingsDropdown"')
if dd_start >= 0:
    dd_end = html.find('</div>', dd_start) + 6
    # Find the right closing div
    depth = 0
    for i in range(dd_start, len(html)):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                dd_end = i + 6
                break
    dd_section = html[dd_start:dd_end]
    with open('D:/tokai/dropdown_section.txt', 'w', encoding='utf-8') as f:
        f.write(dd_section)
    print(f"Dropdown section: {len(dd_section)} chars")
    print("Written to D:/tokai/dropdown_section.txt")

ssh.close()
