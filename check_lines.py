with open('D:/tokai/index-fixed-final.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script>')
end = html.rfind('</script>')
js = html[start+8:end]
lines = js.split('\n')

# Show lines 30-45
for i in range(29, min(45, len(lines))):
    print(f"{i+1}: {lines[i][:100]}")

# Check if nav_portfolio line has comma
line35 = lines[34] if len(lines) > 34 else ''
print(f"\nLine 35 ends with: '{line35.rstrip()[-20:]}'")
print(f"Line 36 starts with: '{lines[35].strip()[:30]}'" if len(lines) > 35 else "no line 36")
