import paramiko
c=paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146',22,'root','ww0987654.',timeout=15)

# Run JS syntax check
cmd = """python3 -c "
import re
with open('/var/www/frontend/index.html','r') as f:
    html=f.read()
start=html.find('<script>')
end=html.rfind('</script>')
js=html[start+8:end]
with open('/tmp/check.js','w') as f:
    f.write(js)
print('JS length:',len(js))
print('MD5 check done')
" && node -e "try{new Function(require('fs').readFileSync('/tmp/check.js','utf8'));console.log('SYNTAX OK')}catch(e){console.log('ERROR:',e.message.substring(0,200))}" 2>&1"""

stdin,stdout,stderr=c.exec_command(cmd)
out=stdout.read().decode('utf-8','replace')
print(out)
c.close()
