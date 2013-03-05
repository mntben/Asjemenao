#include "server.h"
#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/select.h>
#include <sys/time.h>
#include <cstring>

using namespace std;

bool TcpIpServer::acceptConnection()
{
    if (d_list_s == 0)
        return false;
    if (not d_listening)
    {
        cerr << "[MotionController] No listening socket available\n";
        return false;
    }

    timeval time_struct;
    time_struct.tv_sec = 0;
    time_struct.tv_usec = 500000;

    fd_set rfds;
    FD_ZERO(&rfds);
    FD_SET(d_list_s, &rfds);

    int retval = select(d_list_s + 1, &rfds, 0, 0, &time_struct);

    if (retval == -1)
    {
        cerr << "[MotionController] SERVER: Error " << errno << " calling select(): " << strerror(errno) << endl;
        cerr << "FD: " << d_list_s << endl;
        return false;
    }
    else if (retval)
    {
        // There is an incoming connection, accept() it
        if ((d_conn_s = accept(d_list_s, NULL, NULL)) < 0)
        {
            fprintf(stderr, "[MotionController] SERVER: Error calling accept()\n");
            return false;
        }

        /*Set connection to nonblocking mode */
        if (fcntl(d_conn_s, F_SETFL, O_NONBLOCK) == -1)
        {
            fprintf(stderr, "[MotionController] SERVER: Error setting connection in nonblocking mode.\n");
        }

        // Set connection block on close for up to 1 second, and then forcefully
        // close the socket. This should avoid the TIME_WAIT state and thus
        // Socket already in use messages.
        linger linger_setting;
        linger_setting.l_onoff = 1;
        linger_setting.l_linger = 5;
        if (setsockopt(d_conn_s, SOL_SOCKET, SO_LINGER, &linger_setting, sizeof(linger)) != 0)
        {
            fprintf(stderr, "[MotionController] SERVER: Error setting connection SO_LINGER parameter.\n");
        }
        return true;
    }
    // No connection to accept
    return false;
}
