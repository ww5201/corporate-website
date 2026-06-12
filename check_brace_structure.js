const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);
const lines = code.split('\n');

// Check function structure around setLang and before loadCases
console.log('=== Function declarations ===');
const funcRegex = /function\s+(\w+)\s*\(/g;
let match;
while ((match = funcRegex.exec(code)) !== null) {
    const lineNum = code.substring(0, match.index).split('\n').length;
    console.log(`  Line ${lineNum}: function ${match[1]}()`);
}

// Check if there's a missing closing brace between setLang and loadCases
// setLang starts at line 243, loadCases at 448
// Let's check brace balance between these
let depth = 0;
let startLine = 242; // 0-indexed for line 243
let endLine = 447; // 0-indexed for line 448

for (let i = startLine; i < endLine && i < lines.length; i++) {
    for (const ch of lines[i]) {
        if (ch === '{') depth++;
        if (ch === '}') depth--;
    }
    if (depth < 0) {
        console.log(`\n❌ NEGATIVE depth at line ${i+1}: ${lines[i].substring(0, 80)}`);
    }
}

console.log(`\nBrace depth from setLang to loadCases: ${depth}`);
console.log('(Should be 0 if properly closed)');

// Now check from start of script to loadCases
depth = 0;
for (let i = 0; i < 447 && i < lines.length; i++) {
    for (const ch of lines[i]) {
        if (ch === '{') depth++;
        if (ch === '}') depth--;
    }
    if (depth < 0) {
        console.log(`\n❌ NEGATIVE depth at line ${i+1}: ${lines[i].substring(0, 80)}`);
    }
}

console.log(`\nBrace depth from start to loadCases: ${depth}`);
