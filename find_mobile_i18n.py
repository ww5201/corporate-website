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

with open('D:/tokai/mobile_i18n.txt', 'w', encoding='utf-8') as f:
    # Find all mobile_ keys
    import re
    keys = re.findall(r'mobile_\w+', js)
    f.write("All mobile_ keys found:\n")
    for k in sorted(set(keys)):
        f.write(f"  {k}\n")

    # Find i18n zh section mobile keys
    zh_start = js.find("zh:{")
    if zh_start >= 0:
        # Find mobile_ keys in zh section
        f.write("\n\nzh mobile keys:\n")
        i = js.find('mobile_', zh_start)
        while i >= 0 and i < zh_start + 5000:
            # Get the key and value
            line_start = js.rfind('\n', 0, i) + 1
            line_end = js.find('\n', i)
            f.write(f"  {js[line_start:line_end].strip()}\n")
            i = js.find('mobile_', i + 1)

print("Done")
ssh.close()
