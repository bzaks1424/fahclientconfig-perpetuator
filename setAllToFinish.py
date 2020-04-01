import socket
import time

hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
octets = hostip.split('.')
slash24 = "%s.%s.%s" % (octets[0], octets[1], octets[2])
####

for octet in range(1, 253):
    tested_ip = "%s.%d" % (slash24, octet)
    print("Testing %s" % tested_ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    offline = sock.connect_ex((tested_ip, 36330))
    if(not offline):
        print("   %s is not offline" % tested_ip)
        print("Sending Auth")
        auth = sock.send(b'auth VMware1!')
        time.sleep(1)
        print("Sending Finish")
        auth = sock.send(b'finish')
        time.sleep(1)
        print("Sending quit")
        auth = sock.send(b'quit')
        time.sleep(1)
        sock.close()
