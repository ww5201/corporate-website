const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');

// Find loadCases function
const start = js.indexOf('async function loadCases');
const nextFn = js.indexOf('\n    function', start + 10);
const nextFn2 = js.indexOf('\n    async function', start + 10);
const end = Math.min(
    nextFn > 0 ? nextFn : js.length,
    nextFn2 > 0 ? nextFn2 : js.length
);

const loadCases = js.substring(start, end);
console.log(`loadCases function (${loadCases.length} chars):`);
console.log('---');
console.log(loadCases.substring(0, 500));
console.log('---');

// Try to parse just the async keyword
try {
    new Function('async');
    console.log('\n"async" alone: OK');
} catch (e) {
    console.log('\n"async" alone ERROR:', e.message);
}

// Try async function
try {
    new Function('async function foo() {}');
    console.log('"async function foo() {}": OK');
} catch (e) {
    console.log('"async function foo() {}" ERROR:', e.message);
}

// Try with await
try {
    new Function('async function foo() { const r = await fetch(1); }');
    console.log('with await: OK');
} catch (e) {
    console.log('with await ERROR:', e.message);
}
