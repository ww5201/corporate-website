const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check5.js', 'utf8');

// Try parsing line by line to find error location
const lines = js.split('\n');
let bracketDepth = 0;
let parenDepth = 0;
let braceDepth = 0;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    for (const ch of line) {
        if (ch === '{') braceDepth++;
        if (ch === '}') braceDepth--;
        if (ch === '(') parenDepth++;
        if (ch === ')') parenDepth--;
        if (ch === '[') bracketDepth++;
        if (ch === ']') bracketDepth--;
    }
    // Check for negative depth (extra closing bracket)
    if (braceDepth < 0 || parenDepth < 0 || bracketDepth < 0) {
        console.log(`Line ${i+1}: NEGATIVE DEPTH! braces:${braceDepth} parens:${parenDepth} brackets:${bracketDepth}`);
        console.log(`  Content: ${line.substring(0,100)}`);
        console.log(`  Previous: ${lines[i-1]?.substring(0,100) || 'N/A'}`);
    }
}

console.log(`Final: braces:${braceDepth} parens:${parenDepth} brackets:${bracketDepth}`);

// Try to find the function boundary issue
// Look for '}' followed by function declaration without proper separation
let inFunction = false;
for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (trimmed.startsWith('function ') || trimmed.startsWith('async function ')) {
        if (i > 0) {
            const prev = lines[i-1]?.trim();
            if (prev && !prev.endsWith('{') && !prev.endsWith(',') && !prev.endsWith(';') && !prev.endsWith('}') && prev !== '') {
                console.log(`Line ${i+1}: function without separator`);
                console.log(`  Prev: "${prev}"`);
                console.log(`  Curr: "${trimmed}"`);
            }
        }
    }
}
