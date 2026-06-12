import paramiko
c=paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146',22,'root','ww0987654.',timeout=15)

# Check actual file size and content
stdin,stdout,stderr=c.exec_command('wc -c /var/www/frontend/index.html && md5sum /var/www/frontend/index.html')
print(stdout.read().decode())

# Find the exact error location
cmd = """python3 << 'EOF'
import re
with open('/var/www/frontend/index.html','r') as f:
    html=f.read()
start=html.find('<script>')
end=html.rfind('</script>')
js=html[start+8:end]

# Find footer_p1 context
idx=js.find('footer_p1')
if idx>-1:
    context=js[max(0,idx-200):idx+100]
    print('Context around footer_p1:')
    print(repr(context))
else:
    print('footer_p1 not found')
    
# Check for missing commas in i18n
# Find pattern: 'value' followed by newline+spaces+key:
missing_commas = re.findall(r"(:\\s*'[^']+')\\n(\\s+[a-z_]+:)", js)
print(f'\\nMissing commas found: {len(missing_commas)}')
if missing_commas:
    for m in missing_commas[:5]:
        print(f'  {repr(m[0][-30:])} -> {repr(m[1][:30])}')
EOF"""

stdin,stdout,stderr=c.exec_command(cmd)
print(stdout.read().decode())
err=stderr.read().decode()
if err: print('STDERR:',err)
c.close()
