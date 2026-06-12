import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Check what functions are in the HTML but might be missing in JS
# Look for onclick handlers and check if their functions exist
import re

onclick_funcs = set(re.findall(r'onclick="(\w+)\(', html))
script_start = html.find('<script>') + 8
script_end = html.rfind('</script>')
js = html[script_start:script_end]

defined_funcs = set(re.findall(r'function\s+(\w+)', js))

missing = onclick_funcs - defined_funcs

with open('D:/tokai/missing_funcs.txt', 'w', encoding='utf-8') as f:
    f.write(f"onclick functions called: {len(onclick_funcs)}\n")
    f.write(f"JS functions defined: {len(defined_funcs)}\n\n")
    if missing:
        f.write("MISSING FUNCTIONS:\n")
        for m in sorted(missing):
            f.write(f"  - {m}\n")
    else:
        f.write("All onclick functions are defined\n")
    
    # Also check data-i18n onclick
    i18n_onclick = set(re.findall(r'onclick="([^"]+)"', html))
    f.write(f"\nAll onclick handlers: {len(i18n_onclick)}\n")

ssh.close()
print("Done")
