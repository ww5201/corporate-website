import paramiko
c=paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146',22,'root','ww0987654.',timeout=15)

# Extract JS and validate syntax
cmd = """python3 -c "
import re
with open('/var/www/frontend/index.html','r') as f:
    html=f.read()
start=html.find('<script>')
end=html.rfind('</script>')
js=html[start+8:end]
print('JS length:',len(js))
# Write JS to temp file
with open('/tmp/check.js','w') as f:
    f.write(js)
"
node -e "try{new Function(require('fs').readFileSync('/tmp/check.js','utf8'));console.log('JS SYNTAX OK')}catch(e){console.log('JS ERROR:',e.message)}" 2>&1"""

stdin,stdout,stderr=c.exec_command(cmd)
out=stdout.read().decode()
err=stderr.read().decode()
print(out)
if err: print('STDERR:',err)
c.close()
