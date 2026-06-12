import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Get nav section
stdin, stdout, stderr = ssh.exec_command("awk '/<nav/,/<\\/nav>/' /var/www/frontend/index.html")
nav = stdout.read().decode('utf-8')

# Write to file
with open('D:/tokai/nav_structure.txt', 'w', encoding='utf-8') as f:
    f.write(f"NAV HTML:\n{nav}\n")

ssh.close()

print("Saved to D:/tokai/nav_structure.txt")
print(f"Nav length: {len(nav)} chars")
