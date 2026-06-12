with open('D:/tokai/check-final.js', 'r', encoding='utf-8') as f:
    js = f.read()

# The error is "Unexpected identifier 'fetch'" at position 23862
# This means the parser sees 'fetch' as an identifier in an invalid context
# Let's check what's immediately before 'fetch'
pos = 23862
before = js[pos-50:pos]
after = js[pos:pos+50]

with open('D:/tokai/fetch_exact.txt', 'w', encoding='utf-8') as f:
    f.write(f"Before (50 chars):\n{before}\n\nAfter (50 chars):\n{after}\n")
    
# Also check: is there a line that looks like it's missing a semicolon?
# The pattern 'const r = await \n    fetch(...)' suggests the await is on a different line
# This is fine in JS, but let me check if there's something between them

# Check for blank lines between await and fetch
between = js[pos-10:pos]
with open('D:/tokai/fetch_between.txt', 'w', encoding='utf-8') as f:
    f.write(f"Chars between 'await' and 'fetch':\n{repr(between)}\n")

print('wrote')
