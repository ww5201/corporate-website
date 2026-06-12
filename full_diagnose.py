import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Save full file locally
with open('D:/tokai/server_current.html', 'w', encoding='utf-8') as out:
    out.write(html)

# Extract JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

with open('D:/tokai/server_js.txt', 'w', encoding='utf-8') as out:
    out.write(js)

# Run Node.js test with full error capture
test_code = '''
const fs = require('fs');
const js = fs.readFileSync('/tmp/current_js.txt', 'utf8');

// Mock DOM
class MockEl {
    constructor(tag) {
        this.tag = tag; this.style = {}; this.innerHTML = '';
        this.textContent = ''; this.value = ''; this.src = '';
        this.dataset = {}; this.id = ''; this.className = '';
        this.children = []; this.parentNode = null;
        this.classList = { _list: [], add: function(c){this._list.push(c);}, remove: function(c){this._list=this._list.filter(x=>x!==c);}, contains: function(c){return this._list.includes(c);} };
        this._attrs = {};
    }
    appendChild(c) { this.children.push(c); return c; }
    querySelector() { return null; }
    querySelectorAll() { return []; }
    closest() { return null; }
    addEventListener() {}
    removeEventListener() {}
    focus() {}
    setAttribute(k,v) { this._attrs[k]=v; }
    getAttribute(k) { return this._attrs[k]||null; }
    remove() {}
}
globalThis.document = {
    getElementById: () => new MockEl(),
    querySelectorAll: () => [],
    querySelector: () => null,
    createElement: (tag) => new MockEl(tag),
    addEventListener: () => {},
    documentElement: { style: {} },
    body: { appendChild: () => {} }
};
globalThis.window = {
    location: { href: '', reload: () => {}, search: '' },
    addEventListener: () => {},
    setInterval: () => 1,
    clearInterval: () => {},
    setTimeout: () => 1,
    clearTimeout: () => {},
    open: () => {},
    scrollTo: () => {},
    innerWidth: 1024, innerHeight: 768
};
globalThis.localStorage = { getItem: () => null, setItem: () => {}, removeItem: () => {} };
globalThis.fetch = () => Promise.resolve({ json: () => Promise.resolve([]), ok: true, status: 200 });
globalThis.IntersectionObserver = class { constructor(){this.observe=()=>{};this.unobserve=()=>{}} };
globalThis.navigator = { clipboard: { writeText: ()=>Promise.resolve() }, userAgent: 'Test' };
globalThis.console = { log: (...a)=>process.stdout.write('LOG:'+JSON.stringify(a)+'\\n'), error: (...a)=>process.stderr.write('ERR:'+JSON.stringify(a)+'\\n'), warn:()=>{} };
globalThis.alert = () => {};
globalThis.confirm = () => false;
globalThis.Android = { openWechat: ()=>{}, callPhone: ()=>{}, getVersionCode: ()=>3, downloadUpdate: ()=>{} };

try {
    const fn = new Function(js);
    fn();
    process.stdout.write('SUCCESS\\n');
} catch(e) {
    process.stdout.write('CRASH: ' + e.message + '\\n');
    if(e.stack) process.stdout.write('STACK: ' + e.stack.substring(0,800) + '\\n');
}
'''

# Upload JS to server for testing
sftp2 = ssh.open_sftp()
f = sftp2.open('/tmp/current_js.txt', 'w')
f.write(js)
f.close()
f = sftp2.open('/tmp/test_full.js', 'w')
f.write(test_code)
f.close()
sftp2.close()

stdin, stdout, stderr = ssh.exec_command('node /tmp/test_full.js 2>&1')
result = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')

with open('D:/tokai/node_test_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== STDOUT ===\n{result}\n=== STDERR ===\n{err}")

print(f"File size: {len(html)}")
print(f"JS size: {len(js)}")

ssh.close()
