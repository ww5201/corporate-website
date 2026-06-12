const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Show lines 230-245
for (let i = 229; i < 245 && i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i]}`);
}

// Try parsing i18n end to langLabels
console.log('\n=== Testing from i18n end ===');
const i18nEnd = 233; // line 233
for (let end = i18nEnd; end <= 242; end++) {
    const chunk = lines.slice(0, end).join('\n');
    try {
        new Function(chunk);
        console.log(`Lines 1-${end}: OK`);
    } catch (e) {
        console.log(`Lines 1-${end}: ERROR - ${e.message.substring(0, 80)}`);
    }
}
