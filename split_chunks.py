import base64
data = open('D:/tokai/index-fixed2.html','rb').read()
b64 = base64.b64encode(data).decode()
chunk_size = 8000
chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]
print(f'Total b64 length: {len(b64)}')
print(f'Number of chunks: {len(chunks)}')
for i, c in enumerate(chunks):
    open(f'D:/tokai/chunk_{i}.txt','w').write(c)
    print(f'Chunk {i}: {len(c)} chars')
