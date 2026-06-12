with open('D:/tokai/check-final.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find all fetch occurrences
import re
for m in re.finditer(r'\bfetch\b', js):
    pos = m.start()
    # Get surrounding context
    before = js[max(0, pos-200):pos]
    after = js[pos:pos+100]
    
    # Count braces in the 'before' section to understand nesting
    depth = 0
    for ch in before:
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
    
    with open(f'D:/tokai/fetch_ctx_{pos}.txt', 'w', encoding='utf-8') as f:
        f.write(f"Position: {pos}\n")
        f.write(f"Brace depth at this point: {depth}\n")
        f.write(f"\n--- 200 chars before ---\n{before}\n")
        f.write(f"\n--- 100 chars after ---\n{after}\n")
    print(f"fetch at {pos}, depth={depth}, wrote fetch_ctx_{pos}.txt")
