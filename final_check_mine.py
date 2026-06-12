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

with open('D:/tokai/final_mine_check.txt', 'w', encoding='utf-8') as f:
    f.write("=== i18n Check ===\n")
    for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
        f.write("  %s: mobile_mine=%s, mine_title=%s, mine_settings=%s\n" % (
            lang,
            'mobile_mine' in js[js.find(lang+':'):js.find(lang+':')+1500],
            'mine_title' in js[js.find(lang+':'):js.find(lang+':')+1500],
            'mine_settings' in js[js.find(lang+':'):js.find(lang+':')+1500],
        ))

    f.write("\n=== Feature Check ===\n")
    f.write("  showMinePanel: %s\n" % ('function showMinePanel' in js))
    f.write("  hideMinePanel: %s\n" % ('function hideMinePanel' in js))
    f.write("  minePanel HTML: %s\n" % ('id="minePanel"' in html))
    f.write("  mobile_mine in nav: %s\n" % ('mobile_mine' in js))
    f.write("  JS braces: %d:%d\n" % (js.count('{'), js.count('}')))
    f.write("  File: %d bytes\n" % len(html))

print("Done")
ssh.close()
