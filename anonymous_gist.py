import urllib.request, json

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Create anonymous gist via GitHub API (no auth needed for public gists)
data = json.dumps({
    "description": "ZhuoYi fix - index.html",
    "public": True,
    "files": {
        "index.html": {
            "content": html
        }
    }
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.github.com/gists',
    data=data,
    headers={'Content-Type': 'application/json', 'User-Agent': 'ZhuoYi-Fix'}
)

try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    
    raw_url = None
    for fname, finfo in result.get('files', {}).items():
        raw_url = finfo.get('raw_url')
    
    if raw_url:
        print("GIST CREATED!")
        print("URL:", result.get('html_url'))
        print("RAW:", raw_url)
        
        cmd = "wget -O /var/www/frontend/index.html '%s' && nginx -s reload && echo DONE" % raw_url
        
        with open('D:/tokai/workbench_cmd.txt', 'w', encoding='utf-8') as f:
            f.write(cmd)
        
        print("\n=== Workbench 命令: ===")
        print(cmd)
    else:
        print("No raw URL in response")
        print(json.dumps(result, indent=2)[:500])
except Exception as e:
    print("Failed:", e)
