#include "server.h"
#include <fcntl.h>
#include <iostream>


TcpIpServer::TcpIpServer(size_t port)
:
	d_port(port),
	d_list_s(0),
    d_conn_s(0),
    d_running(false),
    d_enslaved(false),
    d_connection_closed(false),
    d_listening(false)
{

    //initialization of private fields:
    sender_state = ST_SEND_IDLE;
    bytes_remaining = 0;
    msg_size = 0;


  
    /*  Create the listening socket  */
    if ( (d_list_s = ::socket(AF_INET, SOCK_STREAM, 0)) < 0 ) {
        fprintf(stderr, "[MotionController] SERVER: Error creating listening socket.\n");
        exit(EXIT_FAILURE);
    }
  
    /*  Set all bytes in socket address structure to
        zero, and fill in the relevant data members   */

    //memset(&servaddr, 0, sizeof(servaddr));
    sockaddr_in servaddr;
    servaddr.sin_family      = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port        = htons(port);
  
    /*  Bind our socket addresss to the 
        listening socket, and call listen()  */
    d_listening = true;
    int res = bind(d_list_s, reinterpret_cast<sockaddr*>(&servaddr), sizeof(servaddr));
    if (res < 0)
    {
        fprintf(stderr, "[MotionController] SERVER: Error calling bind() (port already in use?)\n");
        close(d_list_s);
        d_listening = false;
    }
  
    if (d_listening && listen(d_list_s, LISTENQ) < 0)
    {
        fprintf(stderr, "[MotionController] SERVER: Error calling listen()\n");
        close(d_list_s);
        d_listening = false;
    }
}
