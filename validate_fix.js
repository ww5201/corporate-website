const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final2.js', 'utf-8');
const noAwait = js.replace(/\bawait\s+/g, '');

try {
    new Function(noAwait);
    console.log('JS SYNTAX OK (without await)');
} catch (e) {
    console.log('JS ERROR:', e.message.substring(0, 200));
}

// Also check brace balance
console.log(`Braces: ${js.split('{').length - 1} open, ${js.split('}').length - 1} close`);
console.log(`Functions: ${(js.match(/function\s+\w+/g) || []).length}`);
