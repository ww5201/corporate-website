import urllib.request

# 测试域名访问
try:
    req = urllib.request.Request('http://wgh2026.top/', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=5)
    print(f"wgh2026.top: OK (status {resp.status})")
except Exception as e:
    print(f"wgh2026.top: Failed - {e}")

# 测试www域名
try:
    req = urllib.request.Request('http://www.wgh2026.top/', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=5)
    print(f"www.wgh2026.top: OK (status {resp.status})")
except Exception as e:
    print(f"www.wgh2026.top: Failed - {e}")
