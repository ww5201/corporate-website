import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

path = r'D:\tokai\android-app\app\src\main\java\com\zhuoyi\custom\MainActivity.java'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '        // Initialize WeChat SDK\n        WeChatAuthHelper.init(this);'
new = '        // Initialize WeChat SDK (safe init)\n        try {\n            WeChatAuthHelper.init(this);\n        } catch (Exception e) {\n            // non-fatal\n        }'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - try-catch added")
else:
    print("WARN: pattern not found, checking...")
    idx = content.find('WeChatAuthHelper.init')
    if idx >= 0:
        print(f"Found at index {idx}: ...{content[max(0,idx-40):idx+50]}...")
    else:
        print("WeChatAuthHelper.init NOT found in file!")
