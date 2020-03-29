import socket
import sqlite3
import os
from pathlib import Path

hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
octets = hostip.split('.')
slash24 = "%s.%s.%s" % (octets[0],octets[1],octets[2])
####
appdata = Path(os.environ['APPDATA'])
database_pathobj = appdata / 'FAHClient' / 'FAHControl.db'
if(not database_pathobj.exists()):
    raise Exception("Database Object doesn't exist!")
conn = sqlite3.connect(database_pathobj)
select = "SELECT address FROM clients WHERE address = '%s'"
insert = "REPLACE INTO clients (name, address, port, password) VALUES ( '%s', '%s', 36330, 'VMware1!')"

for octet in range(1, 253):
    tested_ip = "%s.%d" % (slash24, octet)
    print("Testing %s" % tested_ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    offline = sock.connect_ex((tested_ip, 36330))
    if(not offline):
        print("   %s is not offline" % tested_ip)
        curs = conn.cursor()
        selcur = curs.execute(select % tested_ip)
        result = selcur.fetchone()
        if(result is None):
            print("   Need to inject %s in the database" % tested_ip)
            client = "client%s" % octet
            inscur = curs.execute(insert % (client, tested_ip))
            conn.commit()
        selcur.close()
        curs.close()
conn.close()
