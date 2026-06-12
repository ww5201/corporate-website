import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Add toggleMenu function before toggleLang
toggle_menu = """    function toggleMenu() {
      document.getElementById('menu').classList.toggle('show');
    }

    """

if 'function toggleMenu' not in js:
    tl_idx = js.find('function toggleLang')
    if tl_idx >= 0:
        js = js[:tl_idx] + toggle_menu + js[tl_idx:]
        print("Added toggleMenu function")
    else:
        # Add before toggleSettings
        ts_idx = js.find('function toggleSettings')
        if ts_idx >= 0:
            js = js[:ts_idx] + toggle_menu + js[ts_idx:]
            print("Added toggleMenu before toggleSettings")

    # Rebuild HTML
    html = html[:js_start] + js + html[js_end:]

    # Upload
    sftp = ssh.open_sftp()
    f = sftp.open('/var/www/frontend/index.html', 'w')
    f.write(html)
    f.close()
    sftp.close()

    # Verify
    final_js = html[js_start:html.rfind('</script>')]
    print(f"File: {len(html)} bytes, JS braces: {final_js.count(chr(123))}:{final_js.count(chr(125))}")
    print(f"toggleMenu: {'function toggleMenu' in final_js}")
else:
    print("toggleMenu already exists")

ssh.close()
