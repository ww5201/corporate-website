import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check nginx logs for user's requests
stdin, stdout, stderr = ssh.exec_command("tail -50 /var/log/nginx/access.log | head -30")
print("=== Nginx access log (recent) ===")
print(stdout.read().decode())

# Check full JS syntax with Node - find exact line of any problem
stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{const f=new Function(j);console.log('SYNTAX OK');}catch(x){console.log('SYNTAX ERR:'+x.message);const m=x.message.match(/line (\d+)/);if(m){const lines=j.split('\\n');const ln=parseInt(m[1]);for(let i=Math.max(0,ln-5);i<Math.min(lines.length,ln+5);i++){console.log((i+1)+': '+lines[i].substring(0,150))}}}\"")
print("\n=== JS validation ===")
print(stdout.read().decode())

# Actually run the startup code in a sandbox
stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);console.log('JS length:',j.length);console.log('{ count:',(j.match(/{/g)||[]).length);console.log('} count:',(j.match(/}/g)||[]).length);const doc={getElementById:()=>({innerHTML:'',style:{},addEventListener:()=>{},value:'',src:''}),querySelectorAll:()=>[],querySelector:()=>null,createElement:(t)=>({style:{},classList:{add:()=>{},remove:()=>{}},innerHTML:'',src:'',appendChild:()=>{},addEventListener:()=>{}})};globalThis.document=doc;globalThis.window={location:{href:'',reload:()=>{}},addEventListener:()=>{},setInterval:()=>1,clearInterval:()=>{}};globalThis.fetch=()=>Promise.resolve({json:()=>Promise.resolve([])});globalThis.navigator={clipboard:{writeText:()=>Promise.resolve()}};try{Function(j)();console.log('EXEC OK');}catch(x){console.log('EXEC ERR:'+x.message);console.log(x.stack.substring(0,500))}\"")
print(stdout.read().decode())

ssh.close()
