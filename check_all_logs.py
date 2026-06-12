import paramiko, json
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check full JS for any issues
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

js = html[html.find('<script>')+8:html.rfind('</script>')]

# Check for common JS issues
issues = []

# 1. Check all event listener closures
for pattern, name in [
    ('.settings-menu', 'settings-menu class ref'),
    ("currentLangLabel", "currentLangLabel ref"),
    ("target.closest('.settings-dropdown'", "closest settings-dropdown"),
]:
    if pattern in js:
        issues.append(f"Found: {name}")

# 2. Check function signatures for async issues
lines = js.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('function ') and 'async ' not in line[:i] if False else False:
        pass  # Skip this check, too complex

# 3. Write to file and let user check
with open('D:/tokai/issues_report.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total JS length: {len(js)}\n")
    f.write(f"Total lines: {len(lines)}\n")
    f.write(f"Braces: {js.count('{')}:{js.count('}')}\n")
    f.write(f"\nIssues found:\n")
    for issue in issues:
        f.write(f"  {issue}\n")
    f.write(f"\nFirst 10 lines of startup code:\n")
    start_idx = js.find('// =====')
    f.write(js[start_idx:start_idx+500])

print("Report written")

# Check nginx log for recent user requests
stdin, stdout, stderr = ssh.exec_command("tail -20 /var/log/nginx/access.log | grep -v favicon")
access_log = stdout.read().decode('utf-8', errors='replace')
with open('D:/tokai/access_log.txt', 'w', encoding='utf-8') as f:
    f.write(access_log)

# Also check error log
stdin, stdout, stderr = ssh.exec_command("tail -20 /var/log/nginx/error.log 2>/dev/null || echo 'No error log'")
error_log = stdout.read().decode('utf-8', errors='replace')
with open('D:/tokai/nginx_errors.txt', 'w', encoding='utf-8') as f:
    f.write(error_log)

# Check backend error log  
stdin, stdout, stderr = ssh.exec_command('journalctl -u zhuoyi-backend.service --no-pager -n 20 2>/dev/null || echo "No journalctl"')
backend_log = stdout.read().decode('utf-8', errors='replace')
with open('D:/tokai/backend_log.txt', 'w', encoding='utf-8') as f:
    f.write(backend_log)

ssh.close()
