const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);
const lines = code.split('\n');

// Find loadCases function
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('async function loadCases')) {
        console.log(`Found async function loadCases at line ${i+1}`);
        // Show next 20 lines
        for (let j = i; j < i + 20 && j < lines.length; j++) {
            console.log(`  ${j+1}: ${lines[j]}`);
        }
    }
}

// Find all 'await' occurrences
console.log('\n=== All await occurrences ===');
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('await')) {
        // Check if it's inside an async function
        // Find the nearest async function before this line
        let nearestAsync = null;
        for (let j = i; j >= 0; j--) {
            if (lines[j].includes('async function')) {
                nearestAsync = j + 1;
                break;
            }
        }
        console.log(`Line ${i+1}: ${lines[i].trim().substring(0, 80)} (nearest async fn at line ${nearestAsync})`);
    }
}

// Try parsing just the loadCases function definition
const lcStart = code.indexOf('async function loadCases');
let depth = 0;
let lcEnd = lcStart;
for (let i = code.indexOf('{', lcStart); i < code.length; i++) {
    if (code[i] === '{') depth++;
    if (code[i] === '}') depth--;
    if (depth === 0) {
        lcEnd = i + 1;
        break;
    }
}

const lcFn = code.substring(lcStart, lcEnd);
console.log(`\nloadCases function (${lcFn.length} chars):`);
console.log(lcFn);

// Try parsing just loadCases
try {
    new Function(lcFn);
    console.log('\nloadCases alone: OK');
} catch (e) {
    console.log('\nloadCases alone ERROR:', e.message);
    
    // Try with explicit async
    try {
        eval('(' + lcFn + ')');
        console.log('eval: OK');
    } catch (e2) {
        console.log('eval ERROR:', e2.message);
    }
}
