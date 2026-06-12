import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

with open('D:/tokai/problem_areas.txt', 'w', encoding='utf-8') as f:
    # Check showContact - might be named differently
    f.write("=== showContact search ===\n")
    for keyword in ['showContact', 'contact', 'scrollTo.*contact', 'openContact']:
        import re
        matches = re.findall(keyword, html)
        f.write("  '%s': %d occurrences\n" % (keyword, len(matches)))
    
    # Find mine panel section - check for z-index issues
    f.write("\n=== Mine Panel HTML ===\n")
    mine_start = html.find('id="minePanel"')
    if mine_start >= 0:
        f.write(html[max(0,mine_start-100):mine_start+500])
    
    # Check for z-index conflicts
    f.write("\n\n=== Z-index elements ===\n")
    import re
    zindexes = re.findall(r'z-index:\s*(\d+)', html)
    f.write("  z-index values: %s\n" % sorted(set(zindexes), key=int))
    
    # Check if nav has z-index
    nav_idx = html.find('class="nav"')
    if nav_idx >= 0:
        f.write("\n=== Nav CSS ===\n")
        # Find .nav CSS
        css_start = html.find('.nav {')
        if css_start >= 0:
            f.write(html[css_start:css_start+200])
    
    # Check for any broken HTML structure
    f.write("\n\n=== HTML structure ===\n")
    f.write("  <div> count: %d\n" % html.count('<div'))
    f.write("  </div> count: %d\n" % html.count('</div>'))
    f.write("  <script> count: %d\n" % html.count('<script>'))
    f.write("  </script> count: %d\n" % html.count('</script>'))
    f.write("  <style> count: %d\n" % html.count('<style>'))
    f.write("  </style> count: %d\n" % html.count('</style>'))
    
    # Check mine_panel for event issues
    f.write("\n=== Mine Panel functions ===\n")
    js_start = html.find('<script>') + 8
    js_end = html.rfind('</script>')
    js = html[js_start:js_end]
    
    for fn in ['showMinePanel', 'hideMinePanel', 'showLoginPanel', 'showSettingsPanel', 'bindWechat', 'bindPhone', 'clearCache']:
        idx = js.find('function ' + fn)
        if idx >= 0:
            f.write("\n%s:\n" % fn)
            f.write(js[idx:idx+200])
            f.write("\n")

print("Done")
ssh.close()
