import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=15)

# Upload the locally fixed file first
sftp = c.open_sftp()
sftp.put('D:/tokai/index-fixed2.html', '/var/www/frontend/index.html')
print("Uploaded original fixed file")
sftp.close()

# Now run the comma fix on the server directly using Python
cmd = r"""python3 << 'PYEOF'
import re

with open('/var/www/frontend/index.html', 'r') as f:
    html = f.read()

print(f"Before: {len(html)} bytes")

# Find the i18n section
script_start = html.find('<script>')
script_end = html.rfind('</script>')
js = html[script_start+8:script_end]

# Find all places where 'value' is followed by newline + spaces + key: (no comma)
# But only inside the i18n object
i18n_start = js.find('const i18n = {')
if i18n_start == -1:
    print("ERROR: i18n object not found")
else:
    # Find the end of i18n object (matching braces)
    depth = 0
    i18n_end = i18n_start
    for i in range(i18n_start, len(js)):
        if js[i] == '{': depth += 1
        elif js[i] == '}': depth -= 1
        if depth == 0:
            i18n_end = i
            break
    
    i18n_section = js[i18n_start:i18n_end+1]
    print(f"i18n section: {len(i18n_section)} chars")
    
    # Fix missing commas in i18n section
    # Pattern: 'value'\n  key: (missing comma)
    # But NOT 'value',\n  key: (already has comma)
    # And NOT at the end before }
    
    fixed_i18n = i18n_section
    count = 0
    
    # Find all positions where ' is followed by \n (not ,\n)
    positions = []
    for i in range(len(fixed_i18n)):
        if fixed_i18n[i] == "'" and i+1 < len(fixed_i18n) and fixed_i18n[i+1] == '\n':
            # Check if next non-whitespace is an identifier (key:)
            rest = fixed_i18n[i+2:]
            rest_stripped = rest.lstrip()
            if rest_stripped and (rest_stripped[0].isalpha() or rest_stripped[0] == '_'):
                # Check it looks like a key:
                colon_pos = rest_stripped.find(':')
                if 0 < colon_pos < 50:
                    key = rest_stripped[:colon_pos]
                    if all(c.isalnum() or c == '_' for c in key):
                        positions.append(i)
    
    # Apply fixes in reverse order
    for pos in reversed(positions):
        fixed_i18n = fixed_i18n[:pos+1] + ',' + fixed_i18n[pos+1:]
        count += 1
    
    print(f"Added {count} commas in i18n")
    
    # Replace i18n section in JS
    fixed_js = js[:i18n_start] + fixed_i18n + js[i18n_end+1:]
    
    # Replace JS in HTML
    fixed_html = html[:script_start+8] + fixed_js + html[script_end:]
    
    with open('/var/www/frontend/index.html', 'w') as f:
        f.write(fixed_html)
    
    print(f"After: {len(fixed_html)} bytes")
    
    # Validate with node
    with open('/tmp/check.js', 'w') as f:
        f.write(fixed_js)

print("Done - validate with node next")
PYEOF"""

stdin, stdout, stderr = c.exec_command(cmd)
print(stdout.read().decode('utf-8', 'replace'))
err = stderr.read().decode('utf-8', 'replace')
if err: print("STDERR:", err)

# Validate JS syntax
stdin, stdout, stderr = c.exec_command("node -e \"try{new Function(require('fs').readFileSync('/tmp/check.js','utf8'));console.log('JS SYNTAX OK')}catch(e){console.log('JS ERROR:',e.message)}\" 2>&1")
print(stdout.read().decode('utf-8', 'replace'))

# Reload nginx
c.exec_command('nginx -s reload')
print("nginx reloaded")

c.close()
