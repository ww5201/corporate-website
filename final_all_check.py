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

with open('D:/tokai/final_all_check.txt', 'w', encoding='utf-8') as f:
    f.write("=== ALL CHECKS ===\n\n")

    checks = {
        'toggleMenu function': 'function toggleMenu' in js,
        'toggleLang function': 'function toggleLang' in js,
        'toggleSettings function': 'function toggleSettings' in js,
        'setLang function': 'function setLang' in js,
        'showMinePanel function': 'function showMinePanel' in js,
        'hideMinePanel function': 'function hideMinePanel' in js,
        '.menu.show CSS': '.menu.show' in html,
        'minePanel HTML': 'id="minePanel"' in html,
        'langDropdown HTML': 'id="langDropdown"' in html,
        'settingsDropdown HTML': 'id="settingsDropdown"' in html,
        'loadData function': 'async function loadData' in js,
        'loadCases function': 'async function loadCases' in js,
        'renderProducts function': 'function renderProducts' in js,
        'JS syntax OK': True,
    }

    # Check JS syntax
    try:
        # Simple brace balance check
        opens = js.count('{')
        closes = js.count('}')
        if opens != closes:
            checks['JS syntax OK'] = False
            checks['JS braces balanced'] = False
        else:
            checks['JS braces balanced'] = True
    except:
        checks['JS syntax OK'] = False

    # Check i18n mobile_mine for all languages
    for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
        lang_start = js.find(lang + ': {')
        if lang_start < 0:
            lang_start = js.find(lang + ":{")
        if lang_start >= 0:
            has_mine = 'mobile_mine' in js[lang_start:lang_start+1500]
            checks['i18n.%s.mobile_mine' % lang] = has_mine
        else:
            checks['i18n.%s' % lang] = False

    for name, ok in checks.items():
        status = 'OK' if ok else 'MISSING!'
        f.write("  [%s] %s\n" % (status, name))

    f.write("\nJS: %d chars, braces: %d:%d\n" % (len(js), js.count('{'), js.count('}')))
    f.write("File: %d bytes\n" % len(html))

print("Done")
ssh.close()
