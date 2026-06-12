import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download current JS
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

js = html[html.find('<script>')+8:html.rfind('</script>')]

# Write JS to server for testing
f2 = ssh.open_sftp()
f = f2.open('/tmp/fixed_js.txt', 'w')
f.write(js)
f.close()
f2.close()

# Run comprehensive test
test_script = r'''
const fs = require('fs');
const js = fs.readFileSync('/tmp/fixed_js.txt', 'utf8');

class MockEl {
  constructor(tag) {
    this.tag=tag;this.style={};this.innerHTML='';this.textContent='';
    this.value='';this.src='';this.dataset={};this.id='';this.className='';
    this.children=[];this.parentNode=null;
    this.classList={_list:[],add(c){this._list.push(c);},remove(c){this._list=this._list.filter(x=>x!==c);},contains(c){return this._list.includes(c);}};
    this._attrs={};
    this._listeners=[];
  }
  appendChild(c){this.children.push(c);return c;}
  querySelector(){return null;}
  querySelectorAll(){return {forEach(){}};}
  closest(){return null;}
  addEventListener(){}
  removeEventListener(){}
  focus(){}
  setAttribute(k,v){this._attrs[k]=v;}
  getAttribute(k){return this._attrs[k]||null;}
  remove(){}
}
globalThis.document={
  getElementById:(id)=>{
    const el=new MockEl(id);
    el.id=id;
    // Return special objects for known IDs
    if(id==='settingsDropdown') return el;
    if(id==='productsGrid') return el;
    if(id==='prodFilters') return el;
    return el;
  },
  querySelectorAll:(sel)=>{return{forEach(fn){}};},
  querySelector:()=>null,
  createElement:(tag)=>new MockEl(tag),
  addEventListener:()=>{},
  documentElement:{style:{}},
  body:{appendChild(){}}
};
globalThis.window={
  location:{href:'',reload:()=>{},search:''},
  addEventListener:()=>{},
  setInterval:()=>1,
  clearInterval:()=>{},
  setTimeout:()=>1,
  clearTimeout:()=>{},
  open:()=>{},
  scrollTo:()=>{},
  innerWidth:1024,innerHeight:768
};
globalThis.localStorage={getItem:()=>null,setItem:()=>{},removeItem:()=>{}};
globalThis.fetch:()=>Promise.resolve({json:()=>Promise.resolve([{name:'test',price:100,category:'test',images:['/uploads/test.jpg'],_id:'1'}]),ok:true,status:200});
globalThis.IntersectionObserver=class{constructor(){this.observe=()=>{};this.unobserve=()=>{};}};
globalThis.navigator={clipboard:{writeText:()=>Promise.resolve()},userAgent:'Test'};
globalThis.console={log:()=>{},error:(...a)=>process.stderr.write('ERR:'+JSON.stringify(a)+'\n'),warn:()=>{}};
globalThis.alert:()=>{};
globalThis.confirm:()=>false;
globalThis.Android={openWechat:()=>{},callPhone:()=>{},getVersionCode:()=>3,downloadUpdate:()=>{}};

try{
  const fn=new Function(js);
  fn();
  process.stdout.write('SUCCESS\n');
}catch(e){
  process.stdout.write('CRASH: '+e.message+'\n');
  if(e.stack) process.stdout.write(e.stack.substring(0,1000)+'\n');
}
'''

stdin, stdout, stderr = ssh.exec_command("cat > /tmp/test_fixed.js << 'ENDOFSCRIPT'\n" + test_script + "\nENDOFSCRIPT")
err = stderr.read().decode()
if err:
    print(f"Write error: {err[:200]}")

stdin, stdout, stderr = ssh.exec_command('node /tmp/test_fixed.js 2>&1')
result = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')

with open('D:/tokai/node_test_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== STDOUT ===\n{result}\n=== STDERR ===\n{err}")

print(result)
if err:
    print(f"STDERR: {err[:500]}")

ssh.close()
