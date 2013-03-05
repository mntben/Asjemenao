#include "server.h"
#include <string>
#include <iostream>
#include <unistd.h>
#include <sstream>

using namespace std;

int main(int argc, char * argv[])
{
    if (argc < 2)
    {
        cout << "provide port number as first argument\n";
        exit(1);
    }
    istringstream strstream(argv[1]);
    size_t portnr;
    strstream >> portnr;
    TcpIpServer serv(portnr);
    while (true)
    {
        cout << "Waiting for connection\n";
        serv.acceptConnection();
        cout << "Connected\n";
        while(true)
        {
            string s = serv.receiveMsg();
            if (s != "")
                cout << s << endl;
            else
                break;
            sleep(1);
        }
        cout << "Disconnected\n";
    }
}
