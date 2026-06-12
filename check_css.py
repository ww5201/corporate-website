import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

# Find CSS media queries and nav styles
css_start = html.find('<style>') + 7
css_end = html.find('</style>')
css = html[css_start:css_end]

# Find all @media blocks
import re
with open('D:/tokai/media_queries.txt', 'w', encoding='utf-8') as f:
    f.write("=== CSS Media Queries ===\n\n")
    for m in re.finditer(r'@media[^{]*\{', css):
        start = m.start()
        # Find matching closing brace
        depth = 0
        for i in range(start, len(css)):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    f.write(css[start:i+1] + "\n\n")
                    break

    # Find nav-related styles
    f.write("=== Nav CSS ===\n\n")
    for m in re.finditer(r'\.nav[^{]*\{', css):
        start = m.start()
        depth = 0
        for i in range(start, len(css)):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    f.write(css[start:i+1] + "\n\n")
                    break

    # Find settings-related styles
    f.write("=== Settings CSS ===\n\n")
    for m in re.finditer(r'settings[^{]*\{', css):
        start = m.start()
        depth = 0
        for i in range(start, len(css)):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    f.write(css[start:i+1] + "\n\n")
                    break

    # Find lang-switch styles
    f.write("=== Lang CSS ===\n\n")
    for m in re.finditer(r'lang[^{]*\{', css):
        start = m.start()
        depth = 0
        for i in range(start, len(css)):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    f.write(css[start:i+1] + "\n\n")
                    break

print("Done")
ssh.close()
