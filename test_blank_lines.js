try {
    new Function('async function foo() {\n\n  try {\n\n    const r = await fetch(1);\n\n  } catch(e) {}\n\n}');
    console.log('with blank lines: OK');
} catch (e) {
    console.log('ERROR:', e.message);
}

// Try without blank lines
try {
    new Function('async function foo() { try { const r = await fetch(1); } catch(e) {} }');
    console.log('without blank lines: OK');
} catch (e) {
    console.log('ERROR:', e.message);
}
