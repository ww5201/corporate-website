import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

with open('D:/tokai/server_now.html', 'w', encoding='utf-8') as out:
    out.write(html)

with open('D:/tokai/check_result3.txt', 'w', encoding='utf-8') as log:
    log.write(f"File size: {len(html)} bytes\n\n")

    # Nav section
    nav_start = html.find('<nav class="nav"')
    nav_end = html.find('</nav>', nav_start) + 6
    nav = html[nav_start:nav_end]
    log.write(f"Nav: {len(nav)} chars\n")
    log.write(f"toggleSettings btn: {'toggleSettings' in html}\n")
    log.write(f"settingsDropdown id: {'settingsDropdown' in html}\n")
    log.write(f"setLang zh btns: {html.count('setLang')}\n")
    log.write("Gear icon: " + ("YES" if '\u2699' in html else "NO") + "\n\n")
    log.write("=== NAV ===\n")
    log.write(nav[:2000])
    log.write("\n\n")

    # JS braces
    js = html[html.find('<script>')+8:html.rfind('</script>')]
    log.write(f"JS: {len(js)} chars, braces: {js.count(chr(123))}:{js.count(chr(125))}\n\n")

    # Check toggleSettings function
    ts_start = js.find('function toggleSettings')
    if ts_start >= 0:
        ts_end = js.find('\n', ts_start + 200)
        log.write(f"toggleSettings function:\n{js[ts_start:ts_start+300]}\n\n")

    # Check settings click-outside handler
    for line in js.split('\n'):
        if 'click' in line and ('settings' in line.lower() or 'dropdown' in line.lower()):
            log.write(f"Click handler: {line.strip()[:150]}\n")

print("Done - check D:/tokai/check_result3.txt")
ssh.close()
