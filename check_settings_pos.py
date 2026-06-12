import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find settings button
settings_idx = html.find('\u2699</button>')
if settings_idx >= 0:
    context = html[max(0, settings_idx-200):settings_idx+500]
    print("Settings button context:")
    print(context)
    print("\n---\n")

# Find settingsDropdown
dd_idx = html.find('id="settingsDropdown"')
if dd_idx >= 0:
    context = html[max(0, dd_idx-100):dd_idx+800]
    print("Settings dropdown context:")
    print(context)

ssh.close()
