path = r'D:\tokai\android-app\app\src\main\java\com\zhuoyi\custom\MainActivity.java'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add try-catch around WeChat init
old = '''        // Initialize WeChat SDK
        WeChatAuthHelper.init(this);'''

new = '''        // Initialize WeChat SDK (safe init)
        try {
            WeChatAuthHelper.init(this);
        } catch (Exception e) {
            // WeChat SDK init failed - non-fatal, login won't work
        }'''

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - try-catch added around WeChat init")
else:
    print("ERROR: pattern not found!")
