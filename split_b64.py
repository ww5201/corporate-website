import base64
data = open('D:/tokai/index-fixed2.html','rb').read()
b64 = base64.b64encode(data).decode()
# Split into chunks of ~10000 chars for aliyun CLI
chunk_size = 10000
chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]
print(f'Total b64: {len(b64)} chars')
print(f'Chunks: {len(chunks)}')
for i, c in enumerate(chunks):
    open(f'D:/tokai/b{i}.txt', 'w').write(c)
    print(f'b{i}.txt: {len(c)} chars')
