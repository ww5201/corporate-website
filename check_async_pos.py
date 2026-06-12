with open('D:/tokai/check-final.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find async function loadCases
import re
m = re.search(r'async\s+function loadCases', js)
if m:
    print(f"Found at {m.start()}: '{m.group()}'")
else:
    print("Not found as 'async function'")
    # Check what's between async and function
    idx = js.find('async')
    if idx >= 0:
        context = js[idx:idx+100]
        print(f"Context: {repr(context)}")

# Try finding just 'async' near 'function loadCases'
idx_async = js.find('async')
idx_func = js.find('function loadCases')
print(f"'async' at {idx_async}, 'function loadCases' at {idx_func}")
if idx_async >= 0 and idx_func >= 0:
    between = js[idx_async:idx_func+len('function loadCases')]
    print(f"Between: {repr(between[:100])}")
