import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find the duplication start point more precisely
# Look for the pattern: </script> followed by <head> or <script>...<head>
# The original v4 should end with: loadCases(); setLang(currentLang); loadData(); </script></body></html>

# Find all occurrences of key markers
markers = ['loadCases()', 'setLang(currentLang)', 'loadData()', '</body>', '</html>', '</script>']
for m in markers:
    positions = []
    start = 0
    while True:
        idx = html.find(m, start)
        if idx < 0:
            break
        positions.append(idx)
        start = idx + 1
    if len(positions) > 1:
        print(f"{m}: {positions}")

# Find "启动" comment which should be near the end
idx = html.find('// ===== 启动 =====')
if idx >= 0:
    print(f"\nStart marker at {idx}:")
    print(repr(html[idx:idx+80]))

# Find the last proper </script> before things go wrong
# Look for the pattern: </script>\n</body>
last_script_body = html.rfind('</script>\n</body>')
print(f"\nLast </script>\\n</body>: {last_script_body}")
if last_script_body > 0:
    print(repr(html[last_script_body:last_script_body+30]))

ssh.close()
