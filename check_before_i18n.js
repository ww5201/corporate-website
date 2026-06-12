const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Show lines 1-35
console.log('=== Lines 1-35 ===');
for (let i = 0; i < 35 && i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i].substring(0, 100)}`);
}

// Test: can we parse just the code before i18n?
console.log('\n=== Test code before i18n ===');
const beforeI18n = lines.slice(0, 30).join('\n');
try {
    new Function(beforeI18n);
    console.log('Code before i18n: OK');
} catch (e) {
    console.log('Code before i18n ERROR:', e.message.substring(0, 200));
}

// Test: code before i18n + first line of i18n
const withI18nStart = lines.slice(0, 31).join('\n');
try {
    new Function(withI18nStart);
    console.log('With i18n start: OK');
} catch (e) {
    console.log('With i18n start ERROR:', e.message.substring(0, 200));
}
