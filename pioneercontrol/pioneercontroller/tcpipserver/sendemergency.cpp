#include "server.h"
#include <string>
#include <iostream>

using namespace std;

void TcpIpServer::sendEmergency()
{
    if (this->sendTick())
    {
        string message = "EMERGENCY \n";
        sendMsg(message);
        sendTick();
    }
}
