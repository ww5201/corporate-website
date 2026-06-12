import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find </body> position
body_end = html.find('</body>')
print(f"</body> at: {body_end}")
print(f"Context (-100 to +20):")
print(repr(html[body_end-100:body_end+20]))

# Find all </script> positions near the end
import re
for m in re.finditer(r'</script>', html):
    pos = m.start()
    if pos > 73000:
        print(f"\n</script> at {pos}: {repr(html[pos:pos+50])}")

ssh.close()
