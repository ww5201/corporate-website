const vm = require('vm');
const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);

// Replace all 'await ' with '' temporarily
const noAwait = code.replace(/\bawait\s+/g, '');

try {
    new Function(noAwait);
    console.log('WITHOUT await: JS SYNTAX OK');
} catch (e) {
    console.log('WITHOUT await ERROR:', e.message.substring(0, 200));
}

// Also try with async IIFE wrapper
const asyncWrapped = '(async function(){\n' + code + '\n})();';
try {
    new vm.Script(asyncWrapped);
    console.log('Async wrapper: OK');
} catch (e) {
    console.log('Async wrapper ERROR:', e.message.substring(0, 200));
}
