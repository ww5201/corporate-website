import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Get exact nav section
stdin, stdout, stderr = ssh.exec_command("awk '/<nav/,/<\\/nav>/' /var/www/frontend/index.html")
nav = stdout.read().decode('utf-8')

# Count occurrences
print(f"settings-menu in HTML: {nav.count('settings-menu')}")
print(f"settings-dropdown in HTML: {nav.count('settings-dropdown')}")
print(f"toggleSettings in HTML: {nav.count('toggleSettings')}")
print(f"lang-switch in HTML: {nav.count('lang-switch')}")

print(f"\n=== FULL NAV HTML ===\n{nav}")

ssh.close()
