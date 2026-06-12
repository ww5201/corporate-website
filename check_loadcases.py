with open('D:/tokai/check-final.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find loadCases function declaration
import re
m = re.search(r'function loadCases\(\)', js)
if m:
    pos = m.start()
    # Show 200 chars before and 300 chars after
    before = js[max(0,pos-100):pos]
    after = js[pos:pos+400]
    with open('D:/tokai/loadcases_full.txt', 'w', encoding='utf-8') as f:
        f.write(f"=== loadCases context ===\n")
        f.write(f"Position: {pos}\n\n")
        f.write(f"--- 100 chars before ---\n{before}\n\n")
        f.write(f"--- 400 chars after ---\n{after}\n")
    print('wrote loadcases_full.txt')
else:
    print('loadCases not found')
