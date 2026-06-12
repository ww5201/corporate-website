import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

changes = []

# Problem 1: Mine panel is AFTER </script> - needs to be BEFORE </script>
# Remove it from current position
mine_start = html.find('<!-- 我的面板 -->')
if mine_start >= 0:
    # Find the end - after minePanelOverlay closing div
    mine_end = html.find('</div>', html.find('minePanelOverlay', mine_start))
    if mine_end >= 0:
        mine_end += 6
        # Also grab any whitespace/newlines after
        while mine_end < len(html) and html[mine_end] in ' \t\n\r':
            mine_end += 1
        mine_html = html[mine_start:mine_end]
        html = html[:mine_start] + html[mine_end:]
        changes.append("Removed mine panel from wrong position")
        
        # Insert before </script>
        script_end = html.rfind('</script>')
        html = html[:script_end] + mine_html + '\n    ' + html[script_end:]
        changes.append("Inserted mine panel before </script>")

# Problem 2: showContact is missing - add it
if 'function showContact' not in html:
    js_insert = """
    function showContact() {
      var el = document.getElementById('contact');
      if (el) el.scrollIntoView({behavior: 'smooth'});
    }
    """
    # Insert after hideMinePanel function
    hide_end = html.find('function showLoginPanel')
    if hide_end >= 0:
        html = html[:hide_end] + js_insert + '\n\n    ' + html[hide_end:]
        changes.append("Added showContact function")

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Verify
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

with open('D:/tokai/fix_result.txt', 'w', encoding='utf-8') as f:
    f.write("Changes: %d\n" % len(changes))
    for c in changes:
        f.write("  %s\n" % c)
    f.write("\nFile: %d bytes\n" % len(html))
    f.write("JS: %d chars, braces: %d:%d\n" % (len(js), js.count('{'), js.count('}')))
    f.write("showContact: %s\n" % ('function showContact' in js))
    f.write("minePanel before script: %s\n" % (html.find('id="minePanel"') < html.find('</script>')))

print("Changes: %d" % len(changes))
for c in changes:
    print("  %s" % c)
print("File: %d bytes" % len(html))
ssh.close()
