import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download remote
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    remote = f.read().decode('utf-8')
sftp.close()

# Read local
with open(r'D:/tokai/index-clean.html', 'r', encoding='utf-8') as f:
    local = f.read()

print(f"Local: {len(local)}")
print(f"Remote: {len(remote)}")
print(f"Diff: {len(remote) - len(local)}")

# Find where they differ
if local == remote:
    print("Files are identical!")
else:
    # Find first difference
    for i in range(min(len(local), len(remote))):
        if local[i] != remote[i]:
            print(f"\nFirst diff at position {i}")
            print(f"Local[{i-20}:{i+20}]: {repr(local[max(0,i-20):i+20])}")
            print(f"Remote[{i-20}:{i+20}]: {repr(remote[max(0,i-20):i+20])}")
            break
    
    # Check if remote has extra content at the end
    if len(remote) > len(local):
        extra = remote[len(local):]
        print(f"\nExtra content at end ({len(extra)} chars):")
        print(repr(extra[:500]))

# Save remote for inspection
with open(r'D:/tokai/remote_debug.html', 'w', encoding='utf-8') as f:
    f.write(remote)
print("\nSaved remote to D:/tokai/remote_debug.html")

ssh.close()
