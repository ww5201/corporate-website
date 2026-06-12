import gzip, os
data = open('D:/tokai/index-fixed2.html','rb').read()
print(f'Original: {len(data)}')
best_size = len(data)
best_lvl = 0
for lvl in range(1, 10):
    c = gzip.compress(data, compresslevel=lvl)
    open(f'D:/tokai/html_{lvl}.gz', 'wb').write(c)
    print(f'Level {lvl}: {len(c)}')
    if len(c) < best_size:
        best_size = len(c)
        best_lvl = lvl
print(f'Best: level {best_lvl} at {best_size} bytes')
