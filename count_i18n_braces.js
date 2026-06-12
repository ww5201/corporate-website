const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Count braces in i18n section (lines 31-233)
let depth = 0;
for (let i = 30; i < 233 && i < lines.length; i++) {
    const line = lines[i];
    for (const ch of line) {
        if (ch === '{') depth++;
        if (ch === '}') depth--;
    }
    if (depth < 0) {
        console.log(`Line ${i+1}: NEGATIVE depth ${depth}: "${line.trim()}"`);
    }
    // Show closing braces
    if (line.includes('}') && !line.includes('{')) {
        console.log(`Line ${i+1}: depth ${depth}: "${line.trim()}"`);
    }
}
console.log(`Final depth: ${depth}`);

// Also check: is there an extra closing brace?
// Count total { and } in i18n section
let opens = 0, closes = 0;
for (let i = 30; i < 233 && i < lines.length; i++) {
    for (const ch of lines[i]) {
        if (ch === '{') opens++;
        if (ch === '}') closes++;
    }
}
console.log(`Opens: ${opens}, Closes: ${closes}`);
