import paramiko
c=paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146',22,'root','ww0987654.',timeout=15)
sftp=c.open_sftp()
sftp.get('/var/www/frontend/index.html','D:/tokai/server_current.html')
print('Downloaded server file')
sftp.close()

# Compare
with open('D:/tokai/index-fixed2.html','rb') as f: local=f.read()
with open('D:/tokai/server_current.html','rb') as f: server=f.read()
print(f'Local: {len(local)} bytes')
print(f'Server: {len(server)} bytes')
print(f'Match: {local == server}')

# Check JS syntax of server file
import subprocess
with open('D:/tokai/server_current.html','r',encoding='utf-8') as f: html=f.read()
start=html.find('<script>')
end=html.rfind('</script>')
js=html[start+8:end]
with open('D:/tokai/server_js.js','w',encoding='utf-8') as f: f.write(js)
print(f'Server JS: {len(js)} chars')

# Check local JS
with open('D:/tokai/index-fixed2.html','r',encoding='utf-8') as f: html2=f.read()
start2=html2.find('<script>')
end2=html2.rfind('</script>')
js2=html2[start2+8:end2]
with open('D:/tokai/local_js.js','w',encoding='utf-8') as f: f.write(js2)
print(f'Local JS: {len(js2)} chars')
