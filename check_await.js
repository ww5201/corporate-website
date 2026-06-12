const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Find all 'await' occurrences
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('await')) {
        console.log(`Line ${i+1}: ${lines[i].trim().substring(0, 100)}`);
    }
}

// Try parsing just the loadCases function
const lcStart = js.indexOf('async function loadCases');
const lcEnd = js.indexOf('\n    }', js.indexOf('\n    }', lcStart) + 1) + 6;
const loadCasesFn = js.substring(lcStart, lcEnd);
console.log(`\nloadCases function (${loadCasesFn.length} chars):`);
try {
    new Function(loadCasesFn);
    console.log('loadCases: OK');
} catch (e) {
    console.log('loadCases ERROR:', e.message);
}

// Try parsing everything from loadCases to the end
const fromLC = js.substring(lcStart);
console.log(`\nFrom loadCases to end (${fromLC.length} chars):`);
try {
    new Function(fromLC);
    console.log('OK');
} catch (e) {
    console.log('ERROR:', e.message.substring(0, 200));
}
