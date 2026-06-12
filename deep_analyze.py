import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read()
sftp.close()
ssh.close()

# Check for BOM or weird bytes
print(f"First 10 bytes: {html[:10]}")
print(f"File size: {len(html)}")

# Check if there's a duplicate </script> issue
script_starts = []
pos = 0
while True:
    idx = html.find('<script>', pos)
    if idx == -1:
        break
    script_starts.append(idx)
    pos = idx + 8

script_ends = []
pos = 0
while True:
    idx = html.find('</script>', pos)
    if idx == -1:
        break
    script_ends.append(idx)
    pos = idx + 9

print(f"\n<script> positions: {script_starts}")
print(f"</script> positions: {script_ends}")

# Check for any characters that might break JS
for i, c in enumerate(html):
    code = ord(c)
    if code > 127 and c not in '，。！？、；：""''（）《》【】·—…':
        # Could be problematic
        if code > 65535:  # Beyond BMP
            print(f"Potential issue at position {i}: U+{code:04X}")
            break

# Check around the script section
for pos in script_starts:
    context = html[pos:pos+50]
    print(f"\nAround <script> at {pos}: {context}")

# Check for duplicate loadData
load_data_count = html.count('loadData')
print(f"\nloadData count: {load_data_count}")

# Check if there's a second <script> that might shadow
if len(script_starts) > 1:
    print(f"\nMULTIPLE SCRIPT TAGS!")
