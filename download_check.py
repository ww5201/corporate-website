import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Write local copy for analysis
with open(r'D:/tokai/server_index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Downloaded: {len(html)} chars")
print(f"Starts with DOCTYPE: {html.startswith('<!DOCTYPE')}")
print(f"Ends with </html>: {html.rstrip().endswith('</html>')}")
print(f"<script> count: {html.count('<script>')}")
print(f"</script> count: {html.count('</script>')}")

# Find script section
script_start = html.find('<script>')
script_end = html.find('</script>', script_start)
if script_start > 0 and script_end > 0:
    js = html[script_start+8:script_end]
    print(f"\nJS length: {len(js)} chars")
    print(f"JS first 100: {js[:100]}")
    print(f"JS last 100: {js[-100:]}")
    
    # Check brace balance
    print(f"\nJS braces: {{={js.count('{{')}} }}={js.count('}}')}")

ssh.close()
