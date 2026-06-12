import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

js = html[html.find('<script>')+8:html.rfind('</script>')]

with open('D:/tokai/revert_verify.txt', 'w', encoding='utf-8') as f:
    f.write("File: %d bytes\nJS: %d chars, braces: %d:%d\n\n" % (len(html), len(js), js.count('{'), js.count('}')))
    
    # Critical functions
    critical = ['toggleMenu', 'toggleLang', 'toggleSettings', 'setLang', 'loadData', 
                'loadCases', 'renderProducts', 'handleWechatClick', 'selectPay', 'submitOrder']
    f.write("=== Critical Functions ===\n")
    for fn in critical:
        f.write("  [%s] %s\n" % ('OK' if ('function %s' % fn) in js else 'MISSING', fn))
    
    # Check mobile nav has 3 tabs (not 4)
    f.write("\n=== Mobile Nav ===\n")
    f.write("  mobile_mine in nav: %s (should be False)\n" % ('mobile_mine' in js[js.find('mobile_consult'):js.find('mobile_consult')+200] if 'mobile_consult' in js else 'N/A'))
    f.write("  showMinePanel in js: %s (should be False)\n" % ('showMinePanel' in js))
    
    # Check mine panel removed
    f.write("\n=== Mine Panel ===\n")
    f.write("  minePanel in HTML: %s (should be False)\n" % ('id="minePanel"' in html))
    
    # Check startup
    f.write("\n=== Startup ===\n")
    st = js.rfind('// ===== ')
    if st >= 0:
        f.write(js[st:st+150])

print("Done")
ssh.close()
