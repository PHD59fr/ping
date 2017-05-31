#!/usr/bin/python

import subprocess
import MySQLdb
import time

dbHost          = "localhost"
dbUsername      = "root"
dbPassword      = ""
dbName          = "ping_db"

def startPing():
    # Get hostList to check if empty
    db          = MySQLdb.connect( dbHost,dbUsername,dbPassword,dbName )
    cursor      = db.cursor()
    ipListHash  = {}
    ipListReq   = cursor.execute( 'SELECT id, INET_NTOA(ip) FROM ips' )
    if ipListReq:
        # Create ipList with ip and id
        for ipId,ip in cursor.fetchall():
            ipListHash[ip] = ipId
        
        # fping need array with all ip to ping
        ips     = [(ip) for ip, ipId in ipListHash.iteritems()]
        ipList  = ' '.join(ips)

        # if ip is present
        if ipList:
            # Create Fping process and capture the return
            process = subprocess.Popen( "fping -C2 -q " + ipList, stderr=subprocess.PIPE, shell=True )
            output  = process.stderr.read()

            # Just transform out on list
            output  = output.split( '\n' )

            # The last line is empty, i remove it
            del output[-1]

            # Explore list and made fields like an array
            for line in output:
                fields = line.strip().split()

                # fields[0] : IP
                # fields[1] : ":"
                # fields[2] : first icmp test
                # fields[3] : second icmp test
                
                ts          = int( time.time() )
                ipToCheck   = fields[0]
                ipId        = ipListHash[ipToCheck]
                ping1       = fields[2]
                ping2       = fields[3]
                
                # if id not found ( normally impossible )
                if ipId:
                    # if timeout => -1
                    if ping1 == "-":
                        ping1 = "-1"
                    if ping2 == "-":
                        ping2 = "-1"
                    
                    # commit
                    cursor.execute( 'INSERT INTO logs ( ipId, ping1, ping2, ts) VALUES ('+str(ipId)+', '+str(ping1)+', '+str(ping2)+', '+str(ts)+')' )

if __name__ == "__main__":
    try:
        ret = ""
        ret = startPing()
    finally:
        if ret:
            print ret
