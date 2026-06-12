const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);
const lines = code.split('\n');

// Show lines 260-330 to see what these isolated braces are
console.log('=== Lines 260-330 ===');
for (let i = 259; i < 330 && i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i]}`);
}
