const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');

// Extract JUST the loadCases function (between async function loadCases and the next function)
const start = js.indexOf('async function loadCases');
// Find the closing brace of loadCases
let depth = 0;
let end = start;
for (let i = js.indexOf('{', start); i < js.length; i++) {
    if (js[i] === '{') depth++;
    if (js[i] === '}') depth--;
    if (depth === 0) {
        end = i + 1;
        break;
    }
}

const loadCasesFn = js.substring(start, end);
console.log(`loadCases: ${loadCasesFn.length} chars`);
console.log(`First 200: ${loadCasesFn.substring(0, 200)}`);
console.log(`Last 100: ${loadCasesFn.substring(loadCasesFn.length - 100)}`);

// Try parsing
try {
    new Function(loadCasesFn);
    console.log('loadCases: OK');
} catch (e) {
    console.log('loadCases ERROR:', e.message);
    
    // Try progressively
    const fnLines = loadCasesFn.split('\n');
    for (let i = 1; i <= fnLines.length; i++) {
        const chunk = fnLines.slice(0, i).join('\n');
        try {
            new Function(chunk);
        } catch (e2) {
            console.log(`Error at line ${i}: ${fnLines[i-1]?.substring(0, 80)}`);
            break;
        }
    }
}
