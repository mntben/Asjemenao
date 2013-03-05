#include "server.h"

void TcpIpServer::stop()
{
    if (d_running)
    {
        d_running = false;
        d_thread.join();
    }
}

