const vm = require('vm');
const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');

// Extract JS
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const jsCode = js.substring(start, end);

// Try vm.Script
try {
    new vm.Script(jsCode);
    console.log('vm.Script: JS SYNTAX OK');
} catch (e) {
    console.log('vm.Script ERROR:', e.message.substring(0, 200));
}

// Also test in actual browser context simulation
// Wrap in IIFE to simulate <script> execution
const wrapped = '(function() {\n' + jsCode + '\n})();';
try {
    new vm.Script(wrapped);
    console.log('Wrapped: OK');
} catch (e) {
    console.log('Wrapped ERROR:', e.message.substring(0, 200));
}

// Show critical section
const lines = jsCode.split('\n');
console.log('\n=== Lines around 35 (zh nav keys) ===');
for (let i = 33; i <= 38; i++) {
    console.log(`${i+1}: ${lines[i]?.substring(0, 120)}`);
}

console.log('\n=== Lines around 58-62 (zh end / en start) ===');
for (let i = 56; i <= 63; i++) {
    console.log(`${i+1}: ${lines[i]?.substring(0, 80)}`);
}
