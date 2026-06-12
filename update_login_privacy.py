import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
f = sftp.file('/var/www/frontend/login.html', 'r')
content = f.read().decode('utf-8', errors='ignore')
f.close()

# Replace the agreement section - change void(0) links to real pages
old_agreement = '<a href="javascript:void(0)">'
# Count occurrences
count = content.count(old_agreement)
print(f'Found {count} occurrences of javascript:void(0) links')

# Replace first occurrence with user agreement (keep as placeholder or link to terms)
# Replace second occurrence with privacy policy
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'agreement' in line.lower() and 'void(0)' in line:
        # Replace the two void(0) links
        # First: user agreement, Second: privacy policy
        lines[i] = line.replace(
            '<a href="javascript:void(0)">',
            '<a href="/privacy.html">',
            1  # only first occurrence in this line
        ).replace(
            '<a href="javascript:void(0)">',
            '<a href="/privacy.html">'
        )
        safe = lines[i].encode('ascii', 'replace').decode('ascii')
        print(f'Updated line {i+1}: {safe}')
        break

# Also add privacy link in the logged-in profile card (before logout button)
for i, line in enumerate(lines):
    if 'btn-logout' in line and 'doLogout' in line:
        # Insert a privacy link before the logout button
        indent = '        '
        lines.insert(i, indent + '<a href="/privacy.html" style="text-decoration:none"><button class="btn-logout" style="color:var(--primary)">? Privacy</button></a>')
        print(f'Inserted privacy link before line {i+1}')
        break

new_content = '\n'.join(lines)

# Backup and write
f = sftp.file('/var/www/frontend/login.html', 'w')
f.write(new_content)
f.close()

print('OK: login.html updated with privacy link')

sftp.close()
ssh.close()
