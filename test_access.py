import urllib.request

# 测试从本地访问
try:
    req = urllib.request.Request('http://8.138.218.146/', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=5)
    print(f"From China: OK (status {resp.status})")
except Exception as e:
    print(f"From China: Failed - {e}")

# 测试从本地访问API
try:
    req = urllib.request.Request('http://8.138.218.146/api/health', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=5)
    print(f"API: OK - {resp.read().decode()[:50]}")
except Exception as e:
    print(f"API: Failed - {e}")
