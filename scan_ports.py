import socket
for port in [22, 80, 3000, 443, 2222]:
    s = socket.socket()
    s.settimeout(5)
    try:
        s.connect(('8.138.218.146', port))
        print('Port %d: OPEN' % port)
        s.close()
    except Exception as e:
        print('Port %d: CLOSED/BLOCKED (%s)' % (port, type(e).__name__))
