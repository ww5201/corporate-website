import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Download HTML
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Run full JS simulation in Node with mocked DOM
# First, extract the JS
js = html[html.find('<script>')+8:html.rfind('</script>')]

# Build a test script that runs the actual JS with mock DOM
test_script = '''
const js = ''' + repr(js) + ''';

// Basic DOM mock
globalThis.document = {
  getElementById: (id) => {
    const el = {
      innerHTML: '',
      style: {},
      textContent: '',
      value: '',
      src: '',
      dataset: {},
      classList: { add: () => {}, remove: () => {} },
      appendChild: (child) => { el.innerHTML += child.outerHTML || ''; },
      querySelector: () => null,
      querySelectorAll: () => [],
      closest: () => null,
      addEventListener: () => {},
      removeEventListener: () => {},
      focus: () => {}
    };
    el.addEventListener = () => {};
    return el;
  },
  querySelectorAll: () => [],
  querySelector: () => null,
  createElement: (tag) => ({
    style: {},
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    innerHTML: '',
    outerHTML: '',
    src: '',
    appendChild: () => {},
    addEventListener: () => {},
    setAttribute: () => {},
    getAttribute: () => null,
    parentNode: { removeChild: () => {} },
    remove: () => {}
  }),
  addEventListener: () => {},
  documentElement: { style: {} },
  createEvent: () => ({ initEvent: () => {} }),
  body: { appendChild: () => {} }
};

globalThis.window = {
  location: { href: '', reload: () => {}, search: '' },
  addEventListener: () => {},
  removeEventListener: () => {},
  setInterval: () => 1,
  clearInterval: () => {},
  setTimeout: () => 1,
  clearTimeout: () => {},
  open: () => {},
  scrollTo: () => {},
  innerWidth: 1024,
  innerHeight: 768
};

globalThis.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

globalThis.fetch = () => Promise.resolve({
  json: () => Promise.resolve([]),
  ok: true,
  status: 200
});

globalThis.IntersectionObserver = class {
  constructor() { this.observe = () => {}; this.unobserve = () => {}; }
};

globalThis.navigator = {
  clipboard: { writeText: () => Promise.resolve() },
  userAgent: 'Mozilla/5.0 Test'
};

globalThis.console = { log: () => {}, error: () => {}, warn: () => {} };
globalThis.alert = () => {};
globalThis.confirm = () => false;

try {
  const fn = new Function(js);
  fn();
  // Check if loadData was called
  console.log('JS EXECUTED SUCCESSFULLY');
} catch(e) {
  console.log('JS ERROR:', e.message);
  console.log('STACK:', e.stack ? e.stack.substring(0, 500) : 'N/A');
}
'''

# Write test to server
stdin, stdout, stderr = ssh.exec_command('cat > /tmp/js_test.js << "EOF"\n' + test_script + '\nEOF')
err = stderr.read().decode()
if err:
    print(f"Write stderr: {err}")

stdin, stdout, stderr = ssh.exec_command('node /tmp/js_test.js 2>&1')
result = stdout.read().decode()
err = stderr.read().decode()
print("Result:", result)
if err:
    print("Errors:", err[:300])

ssh.close()
