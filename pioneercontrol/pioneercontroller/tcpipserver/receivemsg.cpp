#include "server.h"
#include <string>
#include <iostream>

using namespace std;

std::string TcpIpServer::receiveMsg()
{
    /*
    Read a string from the socket.
    Returns "" if there is no data at the socket or the end of the data was reached without encountering a "\n" character.
    Otherwise, returns the read string terminating in the "\n" character
    */
    if (not d_running)
        return "";

    timeval time_struct;
    time_struct.tv_sec = 0;
    time_struct.tv_usec = 10000;

    fd_set rfds, xfds;
    FD_ZERO(&rfds);
    FD_ZERO(&xfds);
    FD_SET(d_conn_s, &rfds);
    FD_SET(d_conn_s, &xfds);

    time_struct = timeval();
    time_struct.tv_sec = 0;
    time_struct.tv_usec = 10000;
    int retval = select(d_conn_s + 1, &rfds, 0, &xfds, &time_struct);


    if (retval == -1)
    {
        cerr << "[MotionController] SERVER: Error calling select()\n";
        return "DISCONNECTED";
    }

    if (retval == 0)
    {
        // No data to read
        return "";
    }

    if (FD_ISSET(d_conn_s, &xfds))
    {
        cerr << "[MotionController] SERVER: Exception on client socket\n";
        return "DISCONNECTED";
    }

    char c;
    std::string message = "";
    bool ended = false;
    while (not ended)
    {
        int rc = read(d_conn_s, &c, 1);
        if (rc == 1)
            message.append(1, c);
            //std::cout << "read char: " << c << std::endl;
        if (c == '\n')
            ended = true;
        if (rc == 0)
            return "DISCONNECTED";
        if (rc < 0)
            return "";
    }
    return message;
}
