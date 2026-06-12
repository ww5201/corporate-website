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

with open('D:/tokai/mine_verify.txt', 'w', encoding='utf-8') as f:
    # Check mobile_mine in i18n
    f.write(f"mobile_mine in zh: {'mobile_mine' in js[js.find('zh:{'):js.find('zh:{')+1000]}\n")
    f.write(f"mobile_mine in en: {'mobile_mine' in js[js.find('en:{'):js.find('en:{')+1000]}\n")
    f.write(f"mobile_mine in ja: {'mobile_mine' in js[js.find('ja:{'):js.find('ja:{')+1000]}\n")
    f.write(f"mine_title in zh: {'mine_title' in js[js.find('zh:{'):js.find('zh:{')+1000]}\n")
    f.write(f"mine_settings in zh: {'mine_settings' in js[js.find('zh:{'):js.find('zh:{')+1000]}\n")
    f.write(f"mine_login in zh: {'mine_login' in js[js.find('zh:{'):js.find('zh:{')+1000]}\n")
    f.write(f"mine_bindwx in zh: {'mine_bindwx' in js[js.find('zh:{'):js.find('zh:{')+1000]}\n")
    f.write(f"mine_bindphone in zh: {'mine_bindphone' in js[js.find('zh:{'):js.find('zh:{')+1000]}\n")

    # Check mobile nav template
    f.write(f"\nshowMinePanel in HTML: {'showMinePanel' in html}\n")
    f.write(f"minePanel in HTML: {'minePanel' in html}\n")
    f.write(f"mobile_mine in nav template: {'mobile_mine' in js}\n")

    # Check JS
    f.write(f"\nJS: {len(js)} chars, braces: {js.count(chr(123))}:{js.count(chr(125))}\n")

    # Check startup
    st_idx = js.rfind('// ===== 启动')
    if st_idx >= 0:
        f.write(f"Startup:\n{js[st_idx:st_idx+200]}\n")

print("Done")
ssh.close()
