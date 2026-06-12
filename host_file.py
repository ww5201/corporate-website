import urllib.request, urllib.parse, json, ssl

# Read fixed file
with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("File size: %d bytes" % len(html))

# Try file.io (simple file hosting)
try:
    ctx = ssl.create_default_context()
    
    # Method 1: Try 0x0.st (null pointer) - simple anonymous file host
    import http.client
    
    # Use filebin.net - no auth needed
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = (
        '--%s\r\n'
        'Content-Disposition: form-data; name="file"; filename="index.html"\r\n'
        'Content-Type: text/html\r\n\r\n'
        '%s\r\n'
        '--%s--\r\n' % (boundary, html, boundary)
    ).encode('utf-8')
    
    req = urllib.request.Request(
        'https://filebin.net',
        data=body,
        headers={'Content-Type': 'multipart/form-data; boundary=%s' % boundary}
    )
    
    resp = urllib.request.urlopen(req, timeout=30)
    result = resp.read().decode()
    print("filebin response:", result[:200])
except Exception as e:
    print("filebin failed:", e)

# Method 2: Try tmpfiles.org
try:
    data = urllib.parse.urlencode({'content': html, 'ext': '.html'}).encode()
    req = urllib.request.Request('https://tmpfiles.org/api/v1/upload', data=data)
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    if result.get('data', {}).get('url'):
        url = result['data']['url']
        print("\nSUCCESS! Download URL:", url)
        print("\n=== 在 Workbench 中粘贴这一行 ===")
        print("wget -O /var/www/frontend/index.html '%s' && nginx -s reload && echo DONE" % url)
except Exception as e:
    print("tmpfiles failed:", e)

# Method 3: Try paste.ee API
try:
    req = urllib.request.Request(
        'https://paste.ee/api',
        data=urllib.parse.urlencode({
            'encryption': 'false',
            'sections[0][name]': 'index-fixed',
            'sections[0][syntax]': 'html',
            'sections[0][contents]': html
        }).encode(),
        method='POST'
    )
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print("paste.ee response:", str(result)[:200])
except Exception as e:
    print("paste.ee failed:", e)

print("\nDone")
