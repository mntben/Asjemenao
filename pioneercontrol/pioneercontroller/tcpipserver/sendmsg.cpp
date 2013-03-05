#include "server.h"
#include <string>
#include <iostream>

using namespace std;

void TcpIpServer::sendMsg(std::string message)
{
    if (this->sender_state != ST_SEND_IDLE) {
        cout << "Invalid sender state!\n";
        return;
    }

    message.copy(this->send_buffer, message.length());
    this->bytes_remaining = this->msg_size = message.length();
    this->sender_state = ST_SEND_BUSY;
}
