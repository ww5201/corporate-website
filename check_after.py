with open('D:/tokai/check-final.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Get text right after i18n object
after = js[18870:19500]
with open('D:/tokai/after_i18n.txt', 'w', encoding='utf-8') as f:
    f.write(after)
print('wrote after_i18n.txt')

# Also check what's at position 18883 exactly
print('At i18n_end:', repr(js[18880:18900]))
