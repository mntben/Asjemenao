#include "functions.h"
#include <iostream>

using namespace std;

vector<TcpIpServer *> connections;
vector<TcpIpServer *> deletedConnections;
std::mutex connection_lock;
bool server_running;
MotionController MC;

void accepted_connection(int s)
{
    connection_lock.lock();
    TcpIpServer *conn = new TcpIpServer(0, s);
    conn->start();
    connections.push_back(conn);
    connection_lock.unlock();
}

void closed_connection(int s)
{
    connection_lock.lock();
    for (vector<TcpIpServer *>::iterator i = connections.begin(); i != connections.end(); ++i)
    {
        if ((*i)->socket() == s)
        {
            if ((*i)->enslaved())
            {
                MC.unregisterClient();
                (*i)->enslave(false);
            }

            //(*i)->stop(); We won't call stop or delete, because this function is called
            //from the TcpIpServer runner.
            //delete *i;
            deletedConnections.push_back(*i);
            connections.erase(i);

            //the delete is not required, Cause the object is still running ... deleting it will cause seg fault
            //
            break;
        }
    }
    connection_lock.unlock();
}

void shutdown()
{
    server_running = false;
}
