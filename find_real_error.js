const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Find the i18n object end
let i18nEnd = 0;
let depth = 0;
let inI18n = false;
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('const i18n = {')) inI18n = true;
    if (inI18n) {
        for (const ch of lines[i]) {
            if (ch === '{') depth++;
            if (ch === '}') depth--;
        }
        if (depth === 0) {
            i18nEnd = i;
            break;
        }
    }
}

console.log(`i18n ends at line ${i18nEnd + 1}`);

// Now try parsing from after i18n to the end, piece by piece
for (let start = i18nEnd + 1; start < lines.length; start++) {
    // Try parsing from line 1 to this line
    const chunk = lines.slice(0, start + 1).join('\n');
    try {
        new Function(chunk);
    } catch (e) {
        if (e.message.includes('fetch') || e.message.includes('await')) {
            // This is the async/await issue - skip
            continue;
        }
        console.log(`Error at line ${start + 1}: ${lines[start]?.substring(0, 80)}`);
        console.log(`  Error: ${e.message.substring(0, 100)}`);
        console.log(`  Prev: ${lines[start-1]?.substring(0, 80)}`);
        console.log(`  Prev2: ${lines[start-2]?.substring(0, 80)}`);
        break;
    }
}

// Alternative: check if the issue is just the async/await
// Try wrapping in async function
const wrapped = '(async function(){' + js + '})';
try {
    new Function(wrapped);
    console.log('\nWrapped in async: OK');
} catch (e) {
    console.log('\nWrapped in async ERROR:', e.message.substring(0, 200));
}
