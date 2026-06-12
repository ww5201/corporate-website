import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

with open('D:/tokai/dup_check.txt', 'w', encoding='utf-8') as out:
    # Find ALL function definitions in JS section
    script_start = html.find('<script>') + 8
    script_end = html.rfind('</script>')
    js = html[script_start:script_end]
    
    import re
    funcs = re.findall(r'function\s+(\w+)', js)
    out.write(f"Total functions: {len(funcs)}\n\n")
    
    # Find duplicates
    from collections import Counter
    dupes = {k: v for k, v in Counter(funcs).items() if v > 1}
    if dupes:
        out.write("DUPLICATE FUNCTIONS:\n")
        for name, count in dupes.items():
            out.write(f"  {name}: {count} times\n")
    else:
        out.write("No duplicate functions\n")

ssh.close()
print("Done")
