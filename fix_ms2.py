import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

ms_idx = html.find("ms: {")

with open('D:/tokai/ms_debug.txt', 'w', encoding='utf-8') as f:
    # Find the mobile_consult in ms section
    mc_idx = html.find("mobile_consult:", ms_idx)
    if mc_idx >= 0:
        f.write("mobile_consult at %d:\n" % mc_idx)
        # Get 300 chars after it
        f.write(html[mc_idx:mc_idx+300])

        # Find the end of this value line
        line_end = html.find('\n', mc_idx)
        # Find next non-whitespace
        next_content = line_end + 1
        while next_content < len(html) and html[next_content] in ' \t\n\r':
            next_content += 1

        f.write("\n\nNext content at %d: %s\n" % (next_content, html[next_content:next_content+50]))

        # Check if mobile_mine already exists after this
        if 'mobile_mine' not in html[mc_idx:mc_idx+500]:
            # Insert after mobile_consult line
            insert = """,\n        mobile_mine: 'Saya', mine_title: 'Akaun Saya', mine_settings: 'Tetapan', mine_login: 'Log Masuk', mine_bindwx: 'Sambung WeChat', mine_bindphone: 'Sambung Telefon', mine_bindwx_hint: 'Log masuk untuk sambung WeChat dan Telefon', mine_logout: 'Log Keluar', mine_version: 'Versi'\n"""
            html = html[:line_end+1] + insert + html[line_end+1:]

            # Upload
            sftp = ssh.open_sftp()
            ff = sftp.open('/var/www/frontend/index.html', 'w')
            ff.write(html)
            ff.close()
            sftp.close()
            f.write("\n\nAdded to ms! File: %d bytes\n" % len(html))
            print("Added to ms")
        else:
            f.write("\n\nmobile_mine already exists!\n")

print("Done")
ssh.close()
