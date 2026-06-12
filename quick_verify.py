import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Quick syntax check
cmd = """node -e 'const fs=require("fs");const js=fs.readFileSync("/tmp/fixed_js.txt","utf8");try{new Function(js);console.log("SYNTAX_OK")}catch(e){console.log("ERROR:",e.message)}'"""
stdin, stdout, stderr = ssh.exec_command(cmd)
result = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(f"Syntax: {result.strip()}")
if err.strip():
    print(f"Err: {err[:200]}")

sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

js = html[html.find('<script>')+8:html.rfind('</script>')]

print(f"\nFile: {len(html)} bytes, JS: {len(js)} chars")
print(f"Braces: {js.count('{')}:{js.count('}')}")

issues = []
for line in js.split('\n'):
    s = line.strip()
    if 'langDropdown' in s and not s.startswith('//'):
        issues.append(f"langDropdown: {s[:80]}")
    if '.settings-menu' in s:
        issues.append(f"settings-menu: {s[:80]}")
    if "getElementById('currentLangLabel')" in s and not s.startswith('//'):
        issues.append(f"currentLangLabel: {s[:80]}")

if issues:
    print("\nREMAINING ISSUES:")
    for i in issues:
        print(f"  {i}")
else:
    print("\nAll known issues fixed!")

startup = js[js.rfind('// ===== 启动'):]
print(f"\nStartup:\n{startup}")

ssh.close()
