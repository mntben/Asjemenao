#include "server.h"
#include <iostream>

using namespace std;

TcpIpServer::~TcpIpServer()
{
    stop();
    if (d_list_s != 0)
    {
        close(d_list_s);
    }
    if (d_conn_s != 0)
    {
        close(d_conn_s);
    }
}
