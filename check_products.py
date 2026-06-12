import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Check renderProducts function
idx = html.find('function renderProducts')
if idx >= 0:
    with open(r'D:/tokai/renderProducts_check.txt', 'w', encoding='utf-8') as f:
        f.write(html[idx:idx+2000])
    print(f"renderProducts at {idx}, saved to file")

# Check if the JS section is complete - look for the end
# Find all function definitions after loadData
js_start = html.find('function loadData')
rest = html[js_start:]
print(f"\nJS from loadData to end: {len(rest)} chars")
print(f"loadCases() call: {rest.find('loadCases()')}")
print(f"setLang call: {rest.find('setLang(currentLang)')}")
print(f"loadData() call: {rest.find('loadData()')}")

# Check for syntax issues - count braces
open_braces = rest.count('{')
close_braces = rest.count('}')
print(f"\nOpen braces: {open_braces}, Close braces: {close_braces}")
print(f"Difference: {open_braces - close_braces}")

# Show last 200 chars of the HTML
with open(r'D:/tokai/html_end.txt', 'w', encoding='utf-8') as f:
    f.write(html[-500:])
print("Last 500 chars saved to html_end.txt")

ssh.close()
