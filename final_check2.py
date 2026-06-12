import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()
ssh.close()

import re
from collections import Counter

# Get JS section
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Find all function definitions
funcs = re.findall(r'function\s+(\w+)', js)

# Find all onclick calls
onclick_calls = set(re.findall(r'onclick="(\w+)\(', html))

# Check missing
missing = onclick_calls - set(funcs)

with open('D:/tokai/final_result.txt', 'w', encoding='utf-8') as out:
    out.write(f"File size: {len(html)}\n")
    out.write(f"JS functions: {len(funcs)}\n")
    out.write(f"Braces: {js.count('{')}:{js.count('}')}\n\n")
    
    # Check all critical features
    critical = {
        'loadData': 'function loadData' in js,
        'renderProducts': 'function renderProducts' in js,
        'loadCases': 'function loadCases' in js,
        'renderPortfolio': 'function renderPortfolio' in js,
        'handleWechatClick': 'function handleWechatClick' in js,
        'Android Bridge': 'window.Android' in js,
        'selectPay': 'function selectPay' in js,
        'submitOrder': 'function submitOrder' in js,
        'openOrder': 'function openOrder' in js,
        'closeOrder': 'function closeOrder' in js,
        'Startup loadData': 'loadData();' in js,
        'Startup loadCases': 'loadCases();' in js,
        'Startup setLang': 'setLang(currentLang)' in js,
    }
    
    for name, ok in critical.items():
        out.write(f"  [{'OK' if ok else 'MISSING'}] {name}\n")
    
    if missing:
        out.write(f"\nMISSING onclick functions: {missing}\n")
    else:
        out.write("\nAll onclick functions are defined\n")
    
    # Check duplicates
    dupes = {k: v for k, v in Counter(funcs).items() if v > 1}
    if dupes:
        out.write(f"\nDUPLICATES: {dupes}\n")
    else:
        out.write("\nNo duplicates\n")

print("Done")
