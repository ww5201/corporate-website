import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

with open('D:/tokai/urgent_check.txt', 'w', encoding='utf-8') as f:
    f.write("File: %d bytes\n\n" % len(html))
    
    # Extract JS
    js_start = html.find('<script>') + 8
    js_end = html.rfind('</script>')
    js = html[js_start:js_end]
    
    f.write("JS: %d chars, braces: %d:%d\n\n" % (len(js), js.count('{'), js.count('}')))
    
    # Check all critical functions
    funcs = ['toggleMenu', 'toggleLang', 'toggleSettings', 'setLang', 'showMinePanel', 
             'hideMinePanel', 'loadData', 'loadCases', 'renderProducts', 'renderPortfolio',
             'selectPay', 'submitOrder', 'openOrder', 'closeOrder', 'handleWechatClick',
             'showContact', 'openLb', 'closeLb', 'navLb', 'openProductLb', 'checkAppUpdate']
    
    f.write("=== Function Check ===\n")
    for func in funcs:
        found = 'function %s' % func in js or 'async function %s' % func in js
        f.write("  [%s] %s\n" % ('OK' if found else 'MISSING', func))
    
    # Check onclick handlers in HTML
    f.write("\n=== onclick handlers in HTML ===\n")
    import re
    onclicks = re.findall(r'onclick="([^"]+)"', html)
    for oc in set(onclicks):
        # Extract function name
        fname = oc.split('(')[0].strip()
        found = 'function %s' % fname in js
        f.write("  [%s] %s (onclick)\n" % ('OK' if found else 'MISSING', fname))
    
    # Check for syntax errors - look for common issues
    f.write("\n=== Common Issues ===\n")
    # Extra closing braces
    lines = js.split('\n')
    depth = 0
    for i, line in enumerate(lines):
        depth += line.count('{') - line.count('}')
        if depth < 0:
            f.write("  NEGATIVE DEPTH at line %d: depth=%d\n" % (i+1, depth))
    
    # Check for duplicate function definitions
    f.write("\n=== Duplicate functions ===\n")
    for func in ['renderProducts', 'renderPortfolio', 'loadData', 'loadCases']:
        count = js.count('function %s' % func)
        if count > 1:
            f.write("  DUPLICATE: %s (%d times)\n" % (func, count))
    
    # Check key CSS classes
    f.write("\n=== CSS Check ===\n")
    f.write("  .menu.show: %s\n" % ('.menu.show' in html))
    f.write("  #minePanel: %s\n" % ('id="minePanel"' in html))
    f.write("  #langDropdown: %s\n" % ('id="langDropdown"' in html))
    
    # Check for duplicate mine_ keys
    f.write("\n=== Duplicate mine keys ===\n")
    mine_count = html.count('mobile_mine')
    f.write("  mobile_mine occurrences: %d\n" % mine_count)
    
    # Find the startup code
    f.write("\n=== Startup ===\n")
    st_idx = js.rfind('// ===== ')
    if st_idx >= 0:
        f.write(js[st_idx:st_idx+200])

print("Done")
ssh.close()
