const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check3.js', 'utf8');

// Try to find where the extra comma is
// Split by lines and find consecutive commas or comma before }
const lines = js.split('\n');
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Find lines with just a comma or trailing comma before }
    if (line.match(/^\s*,\s*$/)) {
        console.log(`Line ${i+1}: STANDALONE COMMA: "${line.trim()}"`);
    }
    if (line.match(/,\s*}/)) {
        console.log(`Line ${i+1}: COMMA BEFORE }: "${line.trim().substring(0,80)}"`);
    }
    // Find double commas
    if (line.includes(',,')) {
        console.log(`Line ${i+1}: DOUBLE COMMA: "${line.trim().substring(0,80)}"`);
    }
}
