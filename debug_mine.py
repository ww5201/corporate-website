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

with open('D:/tokai/i18n_debug.txt', 'w', encoding='utf-8') as f:
    # Find 'mobile_mine' anywhere in JS
    idx = js.find('mobile_mine')
    if idx >= 0:
        f.write("Found 'mobile_mine' at pos %d:\n" % idx)
        f.write(js[max(0,idx-200):idx+200])
    else:
        f.write("'mobile_mine' NOT FOUND in JS\n")

    # Find all occurrences of 'mobile_'
    f.write("\n\nAll 'mobile_' in JS:\n")
    i = 0
    while True:
        idx = js.find('mobile_', i)
        if idx < 0:
            break
        f.write("  pos %d: %s\n" % (idx, js[idx:idx+30].strip()))
        i = idx + 1

print("Done")
ssh.close()
