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

with open('D:/tokai/i18n_obj.txt', 'w', encoding='utf-8') as f:
    # Find i18n = { or const i18n =
    for pattern in ['i18n = {', 'i18n={', 'const i18n', 'var i18n']:
        idx = js.find(pattern)
        if idx >= 0:
            f.write("Found '%s' at %d:\n" % (pattern, idx))
            f.write(js[idx:idx+200])
            f.write("\n\n")
            break

    # Find first occurrence of 'zh':
    idx = js.find("'zh':")
    if idx >= 0:
        f.write("'zh': at %d:\n" % idx)
        f.write(js[idx:idx+300])
        f.write("\n\n")

    # Find mobile_products
    idx = js.find("'mobile_products'")
    if idx >= 0:
        f.write("'mobile_products' at %d:\n" % idx)
        f.write(js[idx-100:idx+200])

print("Done")
ssh.close()
