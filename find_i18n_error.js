const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Find the i18n object
let i18nStart = -1, i18nEnd = -1;
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('const i18n = {')) {
        i18nStart = i;
    }
    if (i18nStart >= 0 && lines[i].trim() === '};' && i > i18nStart + 5) {
        i18nEnd = i;
        break;
    }
}

console.log(`i18n: lines ${i18nStart+1} to ${i18nEnd+1}`);

// Find which language section has the error
// Try parsing up to each language block
let depth = 0;
let langStarts = [];
for (let i = i18nStart; i <= i18nEnd; i++) {
    const line = lines[i].trim();
    if (line.match(/^(zh|en|ja|ko|th|vi|ms):\s*\{/)) {
        langStarts.push({lang: line.split(':')[0], line: i});
    }
}

console.log(`Language blocks: ${langStarts.map(l => l.lang + '@L' + (l.line+1)).join(', ')}`);

// For each language block, try to parse the i18n object up to that point
for (let li = 0; li < langStarts.length; li++) {
    const endLine = li < langStarts.length - 1 ? langStarts[li+1].line - 1 : i18nEnd;
    const chunk = lines.slice(i18nStart, endLine + 1).join('\n');
    // Try to close the object properly
    const testJs = chunk + '\n};';
    try {
        new Function(testJs);
        console.log(`  ${langStarts[li].lang}: OK`);
    } catch (e) {
        console.log(`  ${langStarts[li].lang}: ERROR - ${e.message.substring(0, 100)}`);
    }
}
