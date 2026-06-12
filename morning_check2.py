import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=30)

# Download current HTML and analyze
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost/")
html = stdout.read().decode('utf-8', errors='replace')

import re
script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)

with open('D:/tokai/morning_check.txt', 'w', encoding='utf-8') as f:
    f.write("HTML: %d bytes\n\n" % len(html))
    
    if script_match:
        js = script_match.group(1)
        f.write("JS: %d chars, braces: %d:%d\n\n" % (len(js), js.count('{'), js.count('}')))
        
        for fn in ['loadData', 'loadCases', 'setLang', 'renderProducts', 'toggleMenu', 'toggleLang', 'handleWechatClick', 'showMinePanel']:
            found = 'function %s' % fn in js
            f.write("[%s] %s\n" % ('OK' if found else 'MISSING', fn))
        
        f.write("\ncurrentLangLabel refs: %d\n" % js.count('currentLangLabel'))
        f.write("langDropdown getElementById: %d\n" % js.count("getElementById('langDropdown')"))
        
        # Startup
        st = js.find('// ===== ')
        if st >= 0:
            f.write("\nStartup:\n%s\n" % js[st:st+150])
    else:
        f.write("NO SCRIPT TAG!\n")
    
    # What does the page look like?
    f.write("\n\n=== First 500 chars of HTML ===\n")
    f.write(html[:500])
    
    # Check products section
    f.write("\n\n=== Products section exists: %s ===\n" % ('id="products"' in html))
    f.write("=== Contact section exists: %s ===\n" % ('id="contact"' in html))

print("Done")
ssh.close()
