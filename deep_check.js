const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);
const lines = code.split('\n');

// Look for potential issues:
// 1. Unmatched brackets in strings
// 2. Missing commas
// 3. Unclosed strings

// Check each line for balanced brackets in non-string parts
let inString = false;
let stringChar = '';
let issues = [];

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let depth = 0;
    let parenDepth = 0;
    let bracketDepth = 0;
    let inStr = false;
    let strChar = '';
    
    for (let j = 0; j < line.length; j++) {
        const ch = line[j];
        if (inStr) {
            if (ch === '\\') { j++; continue; }
            if (ch === strChar) inStr = false;
            continue;
        }
        if (ch === "'" || ch === '"') {
            inStr = true;
            strChar = ch;
            continue;
        }
        if (ch === '{') depth++;
        if (ch === '}') depth--;
        if (ch === '(') parenDepth++;
        if (ch === ')') parenDepth--;
        if (ch === '[') bracketDepth++;
        if (ch === ']') bracketDepth--;
    }
    
    if (inStr) {
        issues.push(`Line ${i+1}: Unclosed string: "${line.substring(0, 80)}"`);
    }
    if (depth !== 0) {
        issues.push(`Line ${i+1}: Brace imbalance (${depth}): "${line.substring(0, 80)}"`);
    }
    if (parenDepth < 0) {
        issues.push(`Line ${i+1}: Extra closing paren: "${line.substring(0, 80)}"`);
    }
    if (bracketDepth < 0) {
        issues.push(`Line ${i+1}: Extra closing bracket: "${line.substring(0, 80)}"`);
    }
}

if (issues.length === 0) {
    console.log("No line-level issues found");
} else {
    console.log(`Found ${issues.length} issues:`);
    issues.slice(0, 20).forEach(iss => console.log(`  - ${iss}`));
}

// Check specific problematic patterns
console.log("\n=== Checking for common syntax errors ===");

// Check for '},' missing before next language
const langs = ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms'];
for (let li = 0; li < langs.length; li++) {
    const lang = langs[li];
    const idx = code.indexOf(`${lang}: {`);
    if (idx === -1) {
        console.log(`  ${lang}: NOT FOUND`);
        continue;
    }
    
    // Find the end of this language block
    let depth = 0;
    let end = code.indexOf('{', idx);
    for (let i = end; i < code.length; i++) {
        if (code[i] === '{') depth++;
        if (code[i] === '}') depth--;
        if (depth === 0) {
            // Check if followed by comma
            let next = i + 1;
            while (next < code.length && ' \t\r\n'.includes(code[next])) next++;
            const after = code.substring(next, next + 20);
            
            if (li < langs.length - 1) {
                // Should have comma or }, before next language
                if (!code[i].includes(',') && code[next] !== ',') {
                    console.log(`  ${lang}: Missing comma after closing brace`);
                } else {
                    console.log(`  ${lang}: OK (ends at pos ${i}, after: '${code.substring(next, next+10)}')`);
                }
            } else {
                console.log(`  ${lang}: OK (last language, ends at pos ${i})`);
            }
            break;
        }
    }
}

// Show the actual i18n closing
const i18nIdx = code.indexOf('const i18n = {');
let depth = 0;
let i18nEnd = code.indexOf('{', i18nIdx);
for (let i = i18nEnd; i < code.length; i++) {
    if (code[i] === '{') depth++;
    if (code[i] === '}') depth--;
    if (depth === 0) {
        console.log(`\n=== i18n object ends at position ${i} ===`);
        console.log(code.substring(Math.max(0, i-100), i+20));
        break;
    }
}
