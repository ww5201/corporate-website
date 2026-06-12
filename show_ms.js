const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Show ms section (lines 205-233)
console.log('=== ms section (lines 205-233) ===');
for (let i = 204; i < 233 && i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i]}`);
}
