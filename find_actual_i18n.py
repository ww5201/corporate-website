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

with open('D:/tokai/i18n_actual.txt', 'w', encoding='utf-8') as f:
    # Find all occurrences of 'mobile_mine'
    i = 0
    while True:
        idx = js.find('mobile_mine', i)
        if idx < 0:
            break
        # Get context
        start = max(0, idx - 100)
        end = min(len(js), idx + 100)
        f.write("Found at pos %d:\n" % idx)
        f.write(js[start:end])
        f.write("\n\n---\n\n")
        i = idx + 1

    # Also check: what does "zh: {" look like?
    for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
        idx = js.find(lang + ':')
        if idx >= 0:
            f.write("'%s:' at pos %d: %s\n" % (lang, idx, js[idx:idx+30]))
        else:
            f.write("'%s:' NOT FOUND\n" % lang)

print("Done")
ssh.close()
