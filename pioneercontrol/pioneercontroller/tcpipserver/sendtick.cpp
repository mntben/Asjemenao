#include "server.h"
#include <string>
#include <cstring>
#include <iostream>
#include <errno.h>
#include <sys/select.h>
#include <sys/time.h>

#include <stdio.h>

using namespace std;

bool TcpIpServer::sendTick()
{
    if (not d_running or d_connection_closed)
        return false;

    switch (this->sender_state) {
        case ST_SEND_IDLE:
            return true;
        case ST_SEND_BUSY:
        {
            timeval time_struct;
            time_struct.tv_sec = 0;
            time_struct.tv_usec = 10000;

            fd_set wfds;
            FD_ZERO(&wfds);
            FD_SET(d_conn_s, &wfds);

            time_struct = timeval();
            time_struct.tv_sec = 0;
            time_struct.tv_usec = 10000;
            int retval = select(d_conn_s + 1, 0, &wfds, 0, &time_struct);

            if (retval == -1)
            {
                cout << "[MotionController] SERVER: Error calling select()\n";
            }
            else if (retval == 0)
            {
                cout << "[MotionController] SERVER: Cannot send data now\n";
                return false;
            }

            // Socket is ready to write data
            int n;
            n = send(d_conn_s, send_buffer + (msg_size - bytes_remaining), bytes_remaining, MSG_NOSIGNAL);
            if (n >= 0) 
            {
                this->bytes_remaining -= n;
                if (this->bytes_remaining == 0) 
                {
                    this->sender_state = ST_SEND_IDLE;
                    return true;
                }
            }
            else
            { // some error occurred
                if ((errno == EPIPE) || (errno == ECONNRESET) || (errno == ECONNABORTED))
                { // Connection is closed, make sure we stop trying
                    d_connection_closed = true;
                    cout << "[MotionController] SERVER: Connection closed.\n";
                }
                else if ((errno != EWOULDBLOCK) && (errno != ENOBUFS))
                {
                    char err[64] = "Failed to send, error: ";
                    strcat(err, strerror(errno));
                    cout << "[MotionController] SERVER: sendTick error(" << errno << "): " << err << endl;
                }
            }
            return false;
            break;
        }
        default:
            throw "BUG: Invalid state!";
    }
}
