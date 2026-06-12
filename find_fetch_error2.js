const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);

// Find all fetch occurrences
const fetchPositions = [];
let idx = 0;
while (true) {
    idx = code.indexOf('fetch(', idx);
    if (idx === -1) break;
    // Make sure it's actually 'fetch' keyword, not part of another word
    const before = code[idx-1];
    if (before === '.' || before === '_' || /[a-zA-Z]/.test(before)) {
        idx++;
        continue;
    }
    fetchPositions.push(idx);
    idx++;
}

console.log(`Found ${fetchPositions.length} fetch occurrences at positions:`, fetchPositions);

// For each fetch, try parsing everything up to that point
for (const pos of fetchPositions) {
    // Find the line containing this fetch
    const lineNum = code.substring(0, pos).split('\n').length;
    const lineStart = code.lastIndexOf('\n', pos - 1) + 1;
    const lineEnd = code.indexOf('\n', pos);
    const line = code.substring(lineStart, lineEnd === -1 ? pos + 100 : lineEnd);
    
    // Try parsing up to and including this line
    const chunk = code.substring(0, lineEnd === -1 ? code.length : lineEnd + 1);
    const noAwait = chunk.replace(/\bawait\s+/g, '');
    
    try {
        new Function(noAwait);
        console.log(`  fetch at line ${lineNum}: before this line - OK`);
    } catch (e) {
        console.log(`  fetch at line ${lineNum}: before this line - ERROR: ${e.message.substring(0, 100)}`);
    }
}
