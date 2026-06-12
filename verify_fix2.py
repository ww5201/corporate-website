import re

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if script_match:
    js = script_match.group(1)
    opens = js.count('{')
    closes = js.count('}')
    print("Braces: %d:%d" % (opens, closes))
    
    idx = js.find('hero_badge')
    if idx >= 0:
        context = js[idx-50:idx+50]
        print("hero_badge context: %s" % repr(context))
    
    func_count = len(re.findall(r'function\s+\w+', js))
    print("Functions: %d" % func_count)
    
    startup = js.find('// ===== 启动 =====')
    if startup >= 0:
        print("Startup: OK")
        print(js[startup:startup+100])
else:
    print("NO SCRIPT!")

print("File: %d bytes" % len(html))
