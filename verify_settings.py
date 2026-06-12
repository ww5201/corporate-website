import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download and compare
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    remote = f.read().decode('utf-8')
sftp.close()

with open(r'D:/tokai/index-settings.html', 'r', encoding='utf-8', errors='surrogatepass') as f:
    local = f.read()

print(f"Local: {len(local)}")
print(f"Remote: {len(remote)}")
print(f"Match: {local == remote}")

# Check key elements
has_gear = '\u2699' in remote
has_settings_div = 'id="settingsDropdown"' in remote
has_langs = "setLang('zh')" in remote
has_update = 'checkAppUpdate' in remote

print(f"Gear icon: {has_gear}")
print(f"Settings div: {has_settings_div}")
print(f"Language buttons: {has_langs}")
print(f"Update link: {has_update}")

ssh.close()
