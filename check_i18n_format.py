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

with open('D:/tokai/i18n_format.txt', 'w', encoding='utf-8') as f:
    # Find i18n object
    i18n_idx = js.find('const i18n')
    if i18n_idx < 0:
        i18n_idx = js.find('var i18n')
    if i18n_idx >= 0:
        # Find each language section
        for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
            lang_idx = js.find("'" + lang + "'", i18n_idx)
            if lang_idx >= 0:
                # Get 200 chars around it
                f.write("Lang '%s' at pos %d:\n" % (lang, lang_idx))
                f.write(js[lang_idx:lang_idx+100])
                f.write("\n\n")

print("Done")
ssh.close()
