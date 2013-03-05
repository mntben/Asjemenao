#include "server.h"

std::string TcpIpServer::getBuffer()
{
    d_lock.lock();
    std::string cur = d_buffer;
    d_buffer = std::string("");
    d_lock.unlock();
    return cur;
}
