import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download and check
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    remote = f.read().decode('utf-8')
sftp.close()

# Read local
with open(r'D:/tokai/index-final.html', 'r', encoding='utf-8') as f:
    local = f.read()

print(f"Local: {len(local)}")
print(f"Remote: {len(remote)}")
print(f"Match: {local == remote}")

# Check for dropdown div
has_div_local = '<div class="settings-dropdown"' in local
has_div_remote = '<div class="settings-dropdown"' in remote
print(f"Dropdown div - Local: {has_div_local}, Remote: {has_div_remote}")

# Check for duplicate content
if len(remote) > len(local) + 100:
    # Find where extra content is
    for i in range(len(local)):
        if i >= len(remote) or local[i] != remote[i]:
            print(f"\nFirst diff at {i}")
            print(f"Local: {repr(local[max(0,i-30):i+30])}")
            print(f"Remote: {repr(remote[max(0,i-30):i+30])}")
            break
    
    # Check if remote has content appended
    if remote.startswith(local):
        extra = remote[len(local):]
        print(f"\nExtra content at end ({len(extra)} chars):")
        print(repr(extra[:200]))

ssh.close()
