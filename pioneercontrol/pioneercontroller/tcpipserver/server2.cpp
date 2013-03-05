#include "server.h"
#include <fcntl.h>

TcpIpServer::TcpIpServer(size_t port, int socket)
:
    d_port(port),
    d_list_s(0),
    d_conn_s(socket),
    d_running(false),
    d_enslaved(false),
    d_connection_closed(false),
    d_listening(false)
{

    //initialization of private fields:
    sender_state = ST_SEND_IDLE;
    bytes_remaining = 0;
    msg_size = 0;
  
}
