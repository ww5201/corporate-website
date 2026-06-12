const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);
const lines = code.split('\n');

// Find ALL try blocks and their catch/finally
const tryBlocks = [];
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('try {')) {
        // Find matching catch or finally
        let foundCatch = false;
        for (let j = i + 1; j < lines.length; j++) {
            if (lines[j].includes('} catch') || lines[j].includes('}catch')) {
                foundCatch = true;
                tryBlocks.push({tryLine: i+1, catchLine: j+1, ok: true});
                break;
            }
            if (lines[j].includes('} finally') || lines[j].includes('}finally')) {
                foundCatch = true;
                tryBlocks.push({tryLine: i+1, catchLine: j+1, ok: true});
                break;
            }
        }
        if (!foundCatch) {
            tryBlocks.push({tryLine: i+1, catchLine: 'NONE', ok: false});
        }
    }
}

console.log('=== Try blocks analysis ===');
for (const tb of tryBlocks) {
    if (!tb.ok) {
        console.log(`❌ try at line ${tb.tryLine} has NO catch/finally!`);
        console.log(`   Context:`);
        for (let i = tb.tryLine - 3; i < tb.tryLine + 5; i++) {
            if (i > 0 && i <= lines.length) {
                console.log(`   ${i}: ${lines[i-1]?.substring(0, 100)}`);
            }
        }
    }
}

// Also check for unmatched braces
console.log('\n=== Checking for orphan braces ===');
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    // Check for lines that are just '}'
    if (trimmed === '}' || trimmed.startsWith('}') && !trimmed.includes('{')) {
        // This might be an orphan closing brace
        // Check context
        const prev = i > 0 ? lines[i-1]?.trim() : '';
        const next = i < lines.length - 1 ? lines[i+1]?.trim() : '';
        if (prev === '' && next === '') {
            console.log(`  Line ${i+1}: Isolated '}' surrounded by blank lines`);
        }
    }
}

// Show lines around 440-470 (loadCases area)
console.log('\n=== Lines around loadCases (445-475) ===');
for (let i = 444; i < 475 && i < lines.length; i++) {
    console.log(`${i+1}: ${lines[i]}`);
}
