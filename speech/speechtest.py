import socket
import pickle

class ReceiveSocket(object):
    """class to receive information over tcp/ip socket"""

    def __init__(self, port=50006):
        """Initialize socket and wait for an incoming connection on port"""
        print 'Waiting for connection on port: ', port
        HOST = ''                 # Symbolic name meaning all available interfaces
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        s.listen(1)
        self.conn, addr = s.accept()
        print 'Connected by', addr

    def read(self):
        """
        Wait for data on the socket and read it.
        """
        sdata = self.conn.recv(4096) #Temporary fix for large amounts of data
        if not sdata:
            self.conn.close()
            raise Exception('no valid data received on socket')
        self.conn.send('ok') #so sender knows the message has been read
	return sdata

    def set_blocking(self, value):
        """
        Sets the blocking mode of the underlying socket that is being used for
        communication.
        """
        self.conn.setblocking(value)


if __name__ == "__main__":

    rc = ReceiveSocket(50025)
    while True:
        print "read: ", rc.read()
