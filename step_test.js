const fs = require('fs');
const js = fs.readFileSync('D:/tokai/index-fixed-final.html', 'utf-8');
const start = js.indexOf('<script>') + 8;
const end = js.lastIndexOf('</script>');
const code = js.substring(start, end);

// Split by function declarations and test each chunk
const funcRegex = /^(    )?(async\s+)?function\s+\w+\s*\(/gm;
const chunks = [];
let lastIndex = 0;
let match;

while ((match = funcRegex.exec(code)) !== null) {
    if (match.index > lastIndex) {
        chunks.push({
            start: lastIndex,
            end: match.index,
            label: `before ${match[0].substring(0, 40)}`
        });
    }
    lastIndex = match.index;
}
chunks.push({start: lastIndex, end: code.length, label: 'last function onwards'});

// Now test incrementally
let current = '';
for (let i = 0; i < chunks.length; i++) {
    current += code.substring(chunks[i].start, chunks[i].end);
    const noAwait = current.replace(/\bawait\s+/g, '');
    try {
        new Function(noAwait);
    } catch (e) {
        console.log(`\n❌ FAILS at chunk ${i}: "${chunks[i].label}" (${chunks[i].end} chars)`);
        console.log(`   Error: ${e.message.substring(0, 100)}`);
        // Show the last 500 chars of this chunk
        console.log(`   Last 500 chars: ${current.slice(-500)}`);
        break;
    }
    if (i === chunks.length - 1) {
        console.log(`All chunks OK (${current.length} total chars)`);
    }
}
