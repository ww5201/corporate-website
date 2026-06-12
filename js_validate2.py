import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Write a validation script on server
val_script = """
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);

// Try to parse (stricter than new Function)
try {
    // Wrap in a function to simulate browser context
    const fn = new Function('document', 'window', 'localStorage', 'fetch', 'console', 'alert', js);
    console.log('VALID: JS parsed successfully');
    console.log('Length:', js.length);
    
    // Check for common issues
    const lines = js.split('\\n');
    console.log('Lines:', lines.length);
    
    // Find all function declarations
    const funcs = [];
    const funcRegex = /function\\s+(\\w+)/g;
    let match;
    while ((match = funcRegex.exec(js)) !== null) {
        funcs.push(match[1]);
    }
    console.log('Functions:', funcs.length);
    
    // Check for duplicates
    const seen = {};
    funcs.forEach(f => {
        if (seen[f]) {
            console.log('DUPLICATE:', f);
        }
        seen[f] = true;
    });
    
    // Check startup code
    if (js.includes('loadData();')) {
        console.log('loadData() call: FOUND');
    } else {
        console.log('loadData() call: MISSING!');
    }
    
    if (js.includes('loadCases();')) {
        console.log('loadCases() call: FOUND');
    } else {
        console.log('loadCases() call: MISSING!');
    }
    
} catch(e) {
    console.log('ERROR:', e.message);
    // Try to find the line number
    const lineMatch = e.message.match(/position (\\d+)/);
    if (lineMatch) {
        const pos = parseInt(lineMatch[1]);
        const before = js.substring(Math.max(0, pos-100), pos);
        const after = js.substring(pos, pos+100);
        console.log('Context before error:', before);
        console.log('Context after error:', after);
    }
}
"""

cmd = f"node -e \"{val_script.replace('\"', '\\\"')}\""
stdin, stdout, stderr = ssh.exec_command(cmd)
result = stdout.read().decode()
errors = stderr.read().decode()

with open('D:/tokai/js_final_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"Result:\n{result}\n")
    if errors:
        f.write(f"\nErrors:\n{errors}\n")

ssh.close()
print("Done")
