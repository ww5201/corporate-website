import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Remove the SECOND (duplicate) renderPortfolio
# Find the second one and remove it
script_start = html.find('<script>') + 8
script_end = html.rfind('</script>')
js = html[script_start:script_end]

import re
# Find all renderPortfolio functions
pattern = r'function renderPortfolio'
positions = [m.start() for m in re.finditer(pattern, js)]

if len(positions) >= 2:
    # Get the start of the second function
    second_start = positions[1]
    
    # Find the end of the second function by counting braces
    brace_count = 0
    in_func = False
    func_end = second_start
    for i in range(second_start, len(js)):
        if js[i] == '{':
            brace_count += 1
            in_func = True
        elif js[i] == '}':
            brace_count -= 1
            if in_func and brace_count == 0:
                func_end = i + 1
                break
    
    # Remove from js
    removed = js[second_start:func_end]
    new_js = js[:second_start] + js[func_end:]
    
    # Rebuild HTML
    new_html = html[:script_start] + new_js + html[script_end:]
    
    with open('D:/tokai/fix_result.txt', 'w', encoding='utf-8') as out:
        out.write(f"Removed second renderPortfolio ({len(removed)} chars)\n")
        out.write(f"Old size: {len(html)}\n")
        out.write(f"New size: {len(new_html)}\n")
        
        # Verify no more duplicates
        new_funcs = re.findall(r'function renderPortfolio', new_js)
        out.write(f"renderPortfolio count after fix: {len(new_funcs)}\n")
        
        # Check brace balance
        out.write(f"Braces: open={new_js.count('{')} close={new_js.count('}')}\n")
    
    # Upload
    import base64
    encoded = base64.b64encode(new_html.encode('utf-8')).decode('ascii')
    cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    
    # Clear nginx cache and reload
    ssh.exec_command('nginx -s reload')
    
    import time
    time.sleep(0.5)
    
    # Verify
    stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1/ | wc -c')
    size = stdout.read().decode().strip()
    with open('D:/tokai/fix_result.txt', 'a', encoding='utf-8') as out:
        out.write(f"\nServer curl size: {size}\n")
    
    # Save local
    with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
else:
    with open('D:/tokai/fix_result.txt', 'w', encoding='utf-8') as out:
        out.write(f"Only found {len(positions)} renderPortfolio functions, nothing to remove\n")

ssh.close()
print("Done")
