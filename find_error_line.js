const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');

// Try to parse with acorn or use a different method
// Let's try splitting the JS into chunks and finding which chunk fails
const lines = js.split('\n');

// Binary search for the error
let lo = 0, hi = lines.length;
while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    const chunk = lines.slice(0, mid + 1).join('\n');
    try {
        new Function(chunk);
        lo = mid + 1;
    } catch (e) {
        hi = mid;
    }
}

console.log(`Error near line ${lo + 1}:`);
console.log(`  "${lines[lo]?.substring(0, 100)}"`);
if (lo > 0) console.log(`  Prev: "${lines[lo-1]?.substring(0, 100)}"`);
if (lo > 1) console.log(`  Prev2: "${lines[lo-2]?.substring(0, 100)}"`);
if (lo > 2) console.log(`  Prev3: "${lines[lo-3]?.substring(0, 100)}"`);
