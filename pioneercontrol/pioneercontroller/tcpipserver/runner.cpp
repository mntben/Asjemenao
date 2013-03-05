#include "server.h"
#include <iostream>
#include <sstream>

#include "../functions.h"

using namespace std;

bool is_disconnect(std::string msg)
{
    std::stringstream sstream;
    sstream << msg;
    std::string command;
    sstream >> command;
    command = command.substr(0, 4);
    return command == "disc" or command == "DISC" or
           command == "quit" or command == "QUIT" or
           command == "exit" or command == "EXIT";
}

bool is_shutdown(std::string msg)
{
    std::stringstream sstream;
    sstream << msg;
    std::string command;
    sstream >> command;
    return command == "shutdown" or command == "SHUTDOWN";
}


void TcpIpServer::runner()
{
	bool listener = d_list_s != 0;
    //TcpIpServer *obj = reinterpret_cast<TcpIpServer *>(arg);

    if (listener)
        cout << "[MotionController] Listening thread started\n" << flush;
    else
        cout << "[MotionController] Connection handling thread started\n" << flush;

    while (d_running)
    {
        usleep(100000);
        if (listener)
        {
            if (acceptConnection())
            {
            	cout << "[Main Listening Thread] Making a new thread, and pushing it inside the global vector\n" << endl;
                accepted_connection(d_conn_s);
                d_conn_s = 0;
            }
        }
        else
        {
            sendTick();
            if (d_connection_closed)
            {
                closed_connection(socket());
                break;
            }
            string msg = receiveMsg();
            if (msg.empty())
                continue;

            if (is_disconnect(msg))
            {
                closed_connection(socket());
                //close(d_conn_s); Commented this cause the close_connection() function in function.cpp will call
                //the destructor of this class.
                d_conn_s = 0;
                break;
            }
            if (is_shutdown(msg))
            {
                closed_connection(socket());
                //close(d_conn_s); Commented this cause the close_connection() function in function.cpp will call
                //the destructor of this class.
                d_conn_s = 0;
                shutdown();
                break;
            }

            d_lock.lock();
            d_buffer += msg;
            d_lock.unlock();
        }
    }

    if (listener)
        cout << "[MotionController] Listening thread ended\n" << flush;
    else
        cout << "[MotionController] Connection handling thread ended\n" << flush;
}
