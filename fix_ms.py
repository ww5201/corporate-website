import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Find ms section
ms_idx = html.find("ms: {")
if ms_idx < 0:
    ms_idx = html.find("ms:{")

with open('D:/tokai/ms_check.txt', 'w', encoding='utf-8') as f:
    if ms_idx >= 0:
        f.write("Found 'ms: {' at %d:\n" % ms_idx)
        # Find closing
        section = html[ms_idx:ms_idx+1500]
        f.write(section[:500])
        f.write("\n\nmobile_mine in ms section: %s\n" % ('mobile_mine' in section))

        if 'mobile_mine' not in section:
            # Find the } before the i18n closing
            i18n_close = html.find('\n    };', ms_idx)
            if i18n_close >= 0:
                close_brace = html.rfind('}', ms_idx, i18n_close)
                if close_brace >= 0:
                    insert = """,\n        mobile_mine: 'Saya', mine_title: 'Akaun Saya', mine_settings: 'Tetapan', mine_login: 'Log Masuk', mine_bindwx: 'Sambung WeChat', mine_bindphone: 'Sambung Telefon', mine_bindwx_hint: 'Log masuk untuk sambung WeChat dan Telefon', mine_logout: 'Log Keluar', mine_version: 'Versi'\n"""
                    html = html[:close_brace] + insert + html[close_brace:]
                    f.write("\nAdded mine_ keys to ms!\n")

                    # Upload
                    sftp = ssh.open_sftp()
                    ff = sftp.open('/var/www/frontend/index.html', 'w')
                    ff.write(html)
                    ff.close()
                    sftp.close()
                    print("Added to ms, file: %d bytes" % len(html))
                else:
                    f.write("Close brace not found\n")
            else:
                f.write("i18n close not found\n")
    else:
        f.write("ms section NOT FOUND\n")

print("Done")
ssh.close()
