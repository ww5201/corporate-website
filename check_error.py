import subprocess
result = subprocess.run(['node', '-e', 
    'try{new Function(require("fs").readFileSync("D:/tokai/check3.js","utf8"))}catch(e){console.log(JSON.stringify({msg:e.message.substring(0,300),pos:e.message.indexOf("Unexpected")}))}'],
    capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
