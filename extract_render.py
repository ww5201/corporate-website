f = open('D:/tokai/full_js.txt', 'r', encoding='utf-8')
txt = f.read()
f.close()

idx = txt.find('function renderProducts')
end_idx = txt.find('\n    function', idx + 20)
if end_idx < 0:
    end_idx = txt.find('\n    // ====', idx + 20)

f = open('D:/tokai/render_func.txt', 'w', encoding='utf-8')
f.write(txt[idx:end_idx])
f.close()

print(f"Written {end_idx - idx} chars")
