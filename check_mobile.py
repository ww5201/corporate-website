import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

js = html[html.find('<script>')+8:html.rfind('</script>')]

with open('D:/tokai/mobile_check.txt', 'w', encoding='utf-8') as f:
    # Check menu-toggle
    f.write(f"menu-toggle in HTML: {'menu-toggle' in html}\n")
    f.write(f"toggleMenu in HTML: {'toggleMenu' in html}\n")
    f.write(f"toggleMenu function: {'function toggleMenu' in js}\n")

    # Check mobile menu CSS
    css = html[html.find('<style>')+7:html.find('</style>')]
    f.write(f"\nmenu-toggle CSS: {'menu-toggle' in css}\n")
    f.write(f".menu {{ display:none }} CSS: {'.menu { display:none' in css}\n")
    f.write(f"mobile-nav CSS: {'mobile-nav' in css}\n")

    # Check mobile bottom nav
    f.write(f"\nmobile-nav in HTML: {'mobile-nav' in html}\n")
    f.write(f"bottom-nav in HTML: {'bottom-nav' in html}\n")

    # Find toggleMenu function
    idx = js.find('function toggleMenu')
    if idx >= 0:
        f.write(f"\ntoggleMenu function:\n{js[idx:idx+300]}\n")
    else:
        f.write("\ntoggleMenu function NOT FOUND!\n")

    # Find all onclick handlers
    import re
    onclicks = re.findall(r"onclick=\"(\w+)\(", html)
    f.write(f"\nAll onclick handlers: {sorted(set(onclicks))}\n")

    # Check which handlers are missing functions
    for handler in sorted(set(onclicks)):
        if f'function {handler}' not in js and f'async function {handler}' not in js:
            # Check if it's a keyword or special
            if handler not in ['if', 'else', 'return', 'this']:
                f.write(f"  MISSING function: {handler}\n")

print("Done")
ssh.close()
