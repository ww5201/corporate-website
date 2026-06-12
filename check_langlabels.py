with open('D:/tokai/index-fixed-final.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]
lines = js.split('\n')

# Show lines 235-250
for i in range(234, min(250, len(lines))):
    with open('D:/tokai/langlabels.txt', 'a', encoding='utf-8') as f:
        f.write(f"{i+1}: {lines[i]}\n")

print('wrote langlabels.txt')
