import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

with open('D:/tokai/bottom_nav.txt', 'w', encoding='utf-8') as f:
    # Find mobile-nav
    idx = html.find('mobile-nav')
    if idx >= 0:
        f.write(f"Found 'mobile-nav' at char {idx}\n\n")
        # Get surrounding 2000 chars
        start = max(0, idx - 200)
        end = min(len(html), idx + 2000)
        f.write(html[start:end])
    else:
        f.write("mobile-nav NOT FOUND\n")

        # Find bottom-nav
        idx2 = html.find('bottom-nav')
        if idx2 >= 0:
            f.write(f"\nFound 'bottom-nav' at char {idx2}\n\n")
            start = max(0, idx2 - 200)
            end = min(len(html), idx2 + 2000)
            f.write(html[start:end])
        else:
            f.write("\nbottom-nav NOT FOUND either\n")

            # Find floating buttons
            idx3 = html.find('handleWechatClick')
            if idx3 >= 0:
                f.write(f"\nhandleWechatClick at {idx3}\n")
                start = max(0, idx3 - 500)
                end = min(len(html), idx3 + 500)
                f.write(html[start:end])

print("Done")
ssh.close()
