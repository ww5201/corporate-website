import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=30)

# Check services
cmds = [
    ("Nginx status", "systemctl status nginx --no-pager -l | head -3"),
    ("Backend health", "curl -s http://localhost:3000/api/health"),
    ("Port 80", "ss -tlnp | grep ':80'"),
    ("Port 3000", "ss -tlnp | grep ':3000'"),
    ("File size", "wc -c /var/www/frontend/index.html"),
    ("Last modified", "ls -la /var/www/frontend/index.html"),
    ("Nginx config test", "nginx -t 2>&1"),
]

with open('D:/tokai/server_status.txt', 'w', encoding='utf-8') as f:
    for name, cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
        out = stdout.read().decode('utf-8', errors='replace').strip()
        err = stderr.read().decode('utf-8', errors='replace').strip()
        f.write("=== %s ===\n" % name)
        if out:
            f.write(out + "\n")
        if err:
            f.write("ERR: " + err + "\n")
        f.write("\n")
    
    # Download and check the HTML
    stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost/", timeout=10)
    html = stdout.read().decode('utf-8', errors='replace')
    f.write("=== HTML Size (via curl) ===\n%d bytes\n\n" % len(html))
    
    # Quick JS check
    import re
    m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
    if m:
        js = m.group(1)
        f.write("JS: %d chars, braces: %d:%d\n" % (len(js), js.count('{'), js.count('}')))
        f.write("loadData: %s\n" % ('loadData' in js))
        f.write("renderProducts: %s\n" % ('renderProducts' in js))
        
        # Check for common crash causes
        f.write("currentLangLabel: %d refs\n" % js.count('currentLangLabel'))
        
        # Check startup
        st = js.find('// ===== ')
        if st >= 0:
            f.write("\nStartup:\n%s\n" % js[st:st+200])
    else:
        f.write("NO SCRIPT TAG!\n")
        f.write("First 500 chars:\n%s\n" % html[:500])

print("Done")
ssh.close()
