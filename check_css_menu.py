import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

css = html[html.find('<style>')+7:html.find('</style>')]

with open('D:/tokai/css_menu_check.txt', 'w', encoding='utf-8') as f:
    # Check menu-related CSS
    for keyword in ['menu-toggle', '.menu.show', '.menu.show', 'mobile-nav', 'bottom-nav', '@media']:
        idx = css.find(keyword)
        if idx >= 0:
            # Get surrounding context
            start = max(0, idx - 50)
            end = min(len(css), idx + 200)
            f.write(f"Found '{keyword}' at {idx}:\n  ...{css[start:end]}...\n\n")

    # Check for .menu.show or .menu.active
    f.write(f"\n.menu.show: {'.menu.show' in css}\n")
    f.write(f".menu.active: {'.menu.active' in css}\n")
    f.write(f"mobile-nav: {css.count('mobile-nav')}\n")

print("Done")
ssh.close()
