import urllib.request, json, ssl, base64

# Read fixed file
with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("File: %d bytes" % len(html))

# Check if git/gh CLI available
import subprocess, os, shutil

# Try gh CLI first (fastest)
gh_path = None
for p in ['gh', r'C:\Program Files\GitHub CLI\gh.exe']:
    if shutil.which(p):
        gh_path = p
        break

if gh_path:
    print("Using gh CLI...")
    # Write to temp file
    tmp = os.path.join(os.environ.get('TEMP', 'D:/tokai'), 'zhuoyi-fix.html')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Create gist
    result = subprocess.run(
        [gh_path, 'gist', 'create', tmp,
         '--public', '-d', 'ZhuoYi fix - index.html',
         '-f', 'index.html'],
        capture_output=True, text=True, timeout=30
    )
    
    if result.returncode == 0:
        gist_url = result.stdout.strip()
        raw_url = gist_url.replace('gist.github.com/', 'raw.githubusercontent.com/') + '/raw'
        
        print("\n=== GIST URL: ===")
        print(gist_url)
        print("\n=== RAW URL: ===")
        print(raw_url)
        
        # Generate wget command
        cmd = "wget -O /var/www/frontend/index.html '%s' && nginx -s reload && echo DONE" % raw_url
        
        with open('D:/tokai/workbench_cmd.txt', 'w', encoding='utf-8') as f:
            f.write(cmd)
        
        print("\n=== 在 Workbench 中粘贴这一行: ===")
        print(cmd)
    else:
        print("gh failed:", result.stderr)
else:
    print("No gh CLI found")
    
    # Use GitHub API directly via curl
    print("\nTrying GitHub API via curl...")
    
    # We need a token... let's check if there's one configured
    result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, timeout=10)
    print("gh auth:", result.stdout[:200] if result.returncode == 0 else "not logged in")

print("\nDone")
