import urllib.request

try:
    req = urllib.request.Request('http://8.138.218.146/', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    content = resp.read(200).decode('utf-8', errors='replace')
    print(f'Accessible: Yes')
    print(f'Content: {content[:100]}')
except Exception as e:
    print(f'Accessible: No')
    print(f'Error: {e}')
