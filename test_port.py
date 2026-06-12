import urllib.request
req = urllib.request.Request('http://8.138.218.146:3000/admin.html')
try:
    r = urllib.request.urlopen(req, timeout=5)
    print('External 3000: OK', r.status)
except Exception as e:
    print('External 3000: FAIL -', e)

# Also test port 80
req2 = urllib.request.Request('http://8.138.218.146/admin.html')
try:
    r2 = urllib.request.urlopen(req2, timeout=5)
    print('External 80: OK', r2.status)
except Exception as e:
    print('External 80: FAIL -', e)
