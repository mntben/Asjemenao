from util.threadedsocket import ThreadedSocket

import util.nullhandler
import util.loggingextra
import sys
import logging
import time

if __name__ == '__main__':
    host = "localhost"
    port = 12345
    if len(sys.argv) > 2:
        host = sys.argv[1]
        port = int(sys.argv[2])
    #logging.getLogger('Borg.Brain').addHandler(util.loggingextra.ScreenOutput())
    #logging.getLogger('Borg.Brain').setLevel(logging.INFO)
    sock = ThreadedSocket(host, port, giveup=0, use_pickle=False, server=False)
    sock.start()
    try:
        start = time.time()
        while not sock.connected and time.time() - start < 2:
            time.sleep(0.01)
        if sock.connected:
            sock.send("quit\r\n")
            while sock.connected and time.time() - start < 2:
                time.sleep(0.01)
            if not sock.connected:
                print "Pioneercontroller at %s is running on port %d" % (host, port)
                sys.exit(0)
            else:
                print "Service running at %s on port %d but not behaving properly as pioneercontroller" % (host, port)
                print repr(sock.get_data())
                sys.exit(1)
        else:
            print "Pioneercontroller at %s is not running on port %d" % (host, port)
            sys.exit(1)
    except Exception as e:
        print repr(e)
        raise
    finally:
        sock.close()
