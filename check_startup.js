const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);
const lines = code.split('\n');

// Show the last 30 lines (startup code)
console.log('=== Last 30 lines (startup code) ===');
for (let i = Math.max(0, lines.length - 30); i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i]}`);
}

// Check if there's an unclosed template literal before loadCases
// by examining the content between setLang and loadCases more carefully
console.log('\n=== Template literal check ===');
let inTemplate = false;
let templateStart = -1;
for (let i = 242; i < 447 && i < lines.length; i++) {
    const line = lines[i];
    for (let j = 0; j < line.length; j++) {
        if (line[j] === '`' && (j === 0 || line[j-1] !== '\\')) {
            if (!inTemplate) {
                inTemplate = true;
                templateStart = i + 1;
            } else {
                inTemplate = false;
            }
        }
    }
}

if (inTemplate) {
    console.log(`❌ Unclosed template literal starting at line ${templateStart}`);
} else {
    console.log('All template literals are closed');
}

// Show lines around 276-290 (mobileNav template)
console.log('\n=== mobileNav template (lines 275-292) ===');
for (let i = 274; i < 292 && i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i]}`);
}
