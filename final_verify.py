import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

with open('D:/tokai/final_verify.txt', 'w', encoding='utf-8') as f:
    # Nav
    nav_start = html.find('<nav class="nav"')
    nav_end = html.find('</nav>', nav_start) + 6
    nav = html[nav_start:nav_end]
    f.write("=== NAV ===\n")
    f.write(nav[:2000])
    f.write("\n\n")

    # JS
    js = html[html.find('<script>')+8:html.rfind('</script>')]

    # Check all critical features
    checks = {
        'lang-switch class in HTML': 'lang-switch' in html[:html.find('<script>')],
        'langDropdown in HTML': 'id="langDropdown"' in html,
        'setLang buttons in HTML': html.count("setLang('zh')") >= 2,
        'toggleLang function': 'function toggleLang' in js,
        'toggleSettings function': 'function toggleSettings' in js,
        'setLang function': 'function setLang' in js,
        'langLabels variable': 'langLabels' in js,
        'currentLangLabel in JS': 'currentLangLabel' in js,
        'loadData function': 'async function loadData' in js,
        'loadCases function': 'async function loadCases' in js,
        'renderProducts function': 'function renderProducts' in js,
        'startup loadCases': 'loadCases()' in js[js.rfind('// ====='):],
        'startup setLang': 'setLang(currentLang)' in js[js.rfind('// ====='):],
        'startup loadData': 'loadData()' in js[js.rfind('// ====='):],
    }

    f.write("=== CHECKS ===\n")
    all_ok = True
    for name, ok in checks.items():
        status = 'OK' if ok else 'MISSING!'
        f.write(f"  [{status}] {name}\n")
        if not ok:
            all_ok = False

    f.write(f"\nJS: {len(js)} chars, braces: {js.count(chr(123))}:{js.count(chr(125))}\n")
    f.write(f"{'ALL PASSED' if all_ok else 'SOME FAILED'}\n")

    # Check for missing element references
    f.write("\n=== Element References ===\n")
    for line in js.split('\n'):
        s = line.strip()
        if 'getElementById' in s and not s.startswith('//'):
            ids = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", s)
            for id_val in ids:
                if f'id="{id_val}"' not in html:
                    f.write(f"  MISSING element '{id_val}': {s[:80]}\n")

print("Done")
ssh.close()
