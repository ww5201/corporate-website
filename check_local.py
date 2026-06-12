import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Read local file
with open(r'D:/tokai/index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('D:/tokai/local_check.txt', 'w', encoding='utf-8') as out:
    out.write(f"Local size: {len(html)}\n")
    
    # Extract JS section
    script_start = html.find('<script>') + 8
    script_end = html.rfind('</script>')
    js = html[script_start:script_end]
    
    out.write(f"JS length: {len(js)}\n")
    out.write(f"Braces: open={js.count('{')} close={js.count('}')}\n\n")
    
    # Check for common JS errors
    # 1. Check for unclosed strings
    # 2. Check for missing semicolons (not critical but can cause issues)
    # 3. Check for undefined variables
    
    # Find all function definitions
    import re
    funcs = re.findall(r'function\s+(\w+)', js)
    out.write(f"Functions defined: {len(funcs)}\n")
    for f_name in funcs:
        out.write(f"  - {f_name}\n")
    
    # Check if handleWechatClick uses Android bridge
    if 'window.Android' in js:
        out.write("\n[OK] handleWechatClick uses Android bridge\n")
    elif "weixin://" in js:
        out.write("\n[WARNING] handleWechatClick uses weixin:// URL\n")
    
    # Find the exact handleWechatClick function
    wc_start = js.find('function handleWechatClick')
    if wc_start >= 0:
        wc_end = js.find('\n    }', wc_start) + 5
        wc_func = js[wc_start:wc_end]
        out.write(f"\nhandleWechatClick function:\n{wc_func}\n")
    
    # Check loadData call
    ld_pos = js.find('loadData();')
    if ld_pos >= 0:
        context = js[ld_pos-50:ld_pos+20]
        out.write(f"\nloadData() call context:\n{context}\n")
    
    # Last 200 chars of JS
    out.write(f"\nLast 200 chars of JS:\n{js[-200:]}\n")

ssh.close()
print("Done")
