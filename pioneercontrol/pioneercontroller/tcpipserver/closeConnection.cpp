#include "server.h"
#include <iostream>

using namespace std;

void TcpIpServer::closeConnection()
{
    /*  Close the connected socket  */
    stop();
    cout << "conn: " << d_conn_s << endl;
    if (d_conn_s != 0 && close(d_conn_s) < 0)
    {
        fprintf(stderr, "SERVER: Error calling close()\n");
    }
    d_conn_s = 0;
    cout << "list: " << d_list_s << endl;
    if (d_list_s != 0 && close(d_list_s) < 0)\
    {
        fprintf(stderr, "SERVER: Error calling close()\n");
    }
    d_list_s = 0;
}
