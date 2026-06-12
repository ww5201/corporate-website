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

# Find mobileNav in JS
with open('D:/tokai/mobile_nav_js.txt', 'w', encoding='utf-8') as f:
    idx = js.find('mobileNav')
    if idx >= 0:
        start = max(0, idx - 300)
        end = min(len(js), idx + 800)
        f.write(f"Found at JS pos {idx}:\n")
        f.write(js[start:end])
    else:
        f.write("mobileNav not found in JS\n")
        # Search for bottom nav in JS
        for kw in ['bottom-nav', 'bottomNav', 'mobile-nav', 'mobile_nav']:
            i = js.find(kw)
            if i >= 0:
                f.write(f"\n{kw} at {i}:\n")
                f.write(js[max(0,i-100):i+300])

print("Done")
ssh.close()
