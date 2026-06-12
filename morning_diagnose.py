import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check server status
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/health")
print("Backend health:", stdout.read().decode().strip())

# Check nginx
stdin, stdout, stderr = ssh.exec_command("systemctl status nginx --no-pager -l | head -5")
print("\nNginx:", stdout.read().decode().strip())

# Check what the browser actually gets
stdin, stdout, stderr = ssh.exec_command("curl -sI http://localhost/")
print("\nNginx response headers:")
print(stdout.read().decode())

# Download current HTML and analyze
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost/")
html = stdout.read().decode('utf-8', errors='replace')

print("\nHTML size:", len(html))
print("Contains products section:", 'id="products"' in html)
print("Contains loadData:", 'loadData' in html)
print("Contains setLang:", 'setLang' in html)

# Extract JS
import re
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    js = script_match.group(1)
    print("\nJS length:", len(js))
    print("JS braces: %d:%d" % (js.count('{'), js.count('}')))
    
    # Check if JS is valid
    print("\n=== Critical function check ===")
    for fn in ['loadData', 'loadCases', 'setLang', 'renderProducts', 'toggleMenu', 'toggleLang', 'handleWechatClick']:
        found = 'function %s' % fn in js
        print("  %s: %s" % (fn, "OK" if found else "MISSING!"))
    
    # Check for common crash points
    print("\n=== Crash point check ===")
    print("  currentLangLabel reference:", js.count('currentLangLabel'))
    print("  #langDropdown reference:", js.count("'langDropdown'"))
    print("  #langDropdown getElementById:", js.count("getElementById('langDropdown')"))
    
    # Find startup code
    startup_idx = js.find('// ===== ')
    if startup_idx >= 0:
        print("\n=== Startup ===")
        print(js[startup_idx:startup_idx+150])
else:
    print("NO SCRIPT TAG FOUND!")

# Check access logs for recent requests
stdin, stdout, stderr = ssh.exec_command("tail -20 /var/log/nginx/access.log | grep -v '\\.css\\|\\.js\\|\\.png\\|\\.jpg\\|\\.ico\\|favicon'")
print("\n=== Recent access ===")
print(stdout.read().decode())

ssh.close()
