const fs = require('fs');
const js = fs.readFileSync('D:/tokai/check-final.js', 'utf8');
const lines = js.split('\n');

// Test: parse i18n object with only ms section
const test = `
const i18n = {
  ms: ${lines.slice(204, 232).join('\n')}
};
`;

try {
    new Function(test);
    console.log('ms alone: OK');
} catch (e) {
    console.log('ms alone ERROR:', e.message);
}

// Test: parse i18n with all sections
const fullI18n = lines.slice(30, 233).join('\n');
try {
    new Function(fullI18n);
    console.log('full i18n: OK');
} catch (e) {
    console.log('full i18n ERROR:', e.message);
    
    // Find the exact position
    // Try each language block
    for (const lang of ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']) {
        // Find the line where this lang starts
        let startLine = -1;
        for (let i = 30; i < 233; i++) {
            if (lines[i].trim().startsWith(lang + ': {')) {
                startLine = i;
                break;
            }
        }
        if (startLine === -1) continue;
        
        // Build i18n with only previous sections + this one
        let testLines = lines.slice(30, startLine + 1);
        // Find the end of this section
        let depth = 0;
        let endLine = startLine;
        for (let i = startLine; i < 233; i++) {
            for (const ch of lines[i]) {
                if (ch === '{') depth++;
                if (ch === '}') depth--;
            }
            if (depth === 0) {
                endLine = i;
                break;
            }
        }
        testLines = lines.slice(30, endLine + 1);
        testLines.push('};');
        
        try {
            new Function(testLines.join('\n'));
        } catch (e2) {
            console.log(`  Adding ${lang} breaks it: ${e2.message.substring(0, 100)}`);
            // Show the problematic lines
            for (let i = startLine; i <= endLine; i++) {
                console.log(`    ${i+1}: ${lines[i].substring(0, 80)}`);
            }
        }
    }
}
