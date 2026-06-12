const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Binary search with line granularity
let lo = 0, hi = lines.length;
while (lo < hi - 1) {
    const mid = Math.floor((lo + hi) / 2);
    const chunk = lines.slice(0, mid).join('\n');
    try {
        new Function(chunk);
        lo = mid;
    } catch (e) {
        hi = mid;
    }
}

console.log(`First error at line ${hi}: "${lines[hi-1]?.substring(0, 100)}"`);
console.log(`Previous line ${hi-1}: "${lines[hi-2]?.substring(0, 100)}"`);
console.log(`Two back ${hi-2}: "${lines[hi-3]?.substring(0, 100)}"`);
console.log(`Three back ${hi-3}: "${lines[hi-4]?.substring(0, 100)}"`);
console.log(`Four back ${hi-4}: "${lines[hi-5]?.substring(0, 100)}"`);

// Also show what's around line hi
console.log(`\nContext (lines ${hi-5} to ${hi+5}):`);
for (let i = Math.max(0, hi-6); i < Math.min(lines.length, hi+5); i++) {
    console.log(`  ${i+1}: ${lines[i].substring(0, 100)}`);
}
