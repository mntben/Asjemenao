#include "tcpipserver/server.h"
#include "commandparser/commandparser.h"
#include "motioncontroller/MotionController.h"

#include <iostream>
#include <sstream>
#include <string>
#include <ctime>
#include <unistd.h>
#include "types.h"
#include <pthread.h>
#include <thread>
#include <vector>
#include "functions.h"
#include <time.h>

using namespace std;

size_t getPortNr(int argc, char * argv[])
{
    //get the port number from the command line argument
    if (argc < 2)
    {
        cout << "provide port number as first argument" << endl;
        exit(1);
    }
    
    //convert the first argument (string) to a number
    istringstream strstream(argv[1]);
    size_t portnr;
    strstream >> portnr;
    return portnr;
}

void shutdown_handler(int a)
{
    cout << "[MotionController] Caught signal, quitting" << endl << flush;
    signal(SIGINT, shutdown_handler);
    signal(SIGTERM, shutdown_handler);
    signal(SIGKILL, shutdown_handler);
    signal(SIGHUP, shutdown_handler);
    signal(SIGABRT, shutdown_handler);
    signal(SIGQUIT, shutdown_handler);
    signal(SIGPIPE, shutdown_handler);
    shutdown();
}

double pythonTime()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}

int main(int argc, char * argv[])
{
    cout << "PID: " << getpid() << endl;

    // Catch signal handlers
    signal(SIGINT, shutdown_handler);
    signal(SIGTERM, shutdown_handler);
    signal(SIGKILL, shutdown_handler);
    signal(SIGHUP, shutdown_handler);
    signal(SIGABRT, shutdown_handler);
    signal(SIGQUIT, shutdown_handler);
    signal(SIGPIPE, shutdown_handler);

    server_running = true;

    size_t portnr = getPortNr(argc, argv);
    TcpIpServer *listener = new TcpIpServer(portnr);
    const size_t timeout = 2;
    while (not listener->listening())
    {
        delete listener;
        if (not server_running)
        {
            exit(1);
        }
        cerr << "[MotionController] Cannot bind to port " << portnr 
             << " - retrying in " << timeout << " seconds\n";
        sleep(timeout);
        listener = new TcpIpServer(portnr);
    }

    CommandParser CP;
    try
    {
		listener->start();
		cout << "[MotionController] Now listening on port " << portnr << endl << flush;


		MC.start();
    }
    catch (...)
    {
    	cout << "Listener fail \n";
    };
    std::string message;

    double odo_time = 0;
 
    bool robot_was_working = false;

    while (server_running)
    {
    	size_t maxDeadCons = 5;
    	if (deletedConnections.size() > maxDeadCons)
			for (vector<TcpIpServer *>::iterator i = deletedConnections.begin(); i != deletedConnections.end(); ++i)
			{
				delete *i;
				deletedConnections.erase(i);
			}
        connection_lock.lock();
        for (vector<TcpIpServer *>::iterator i = connections.begin(); i != connections.end(); ++i)
        {
            TcpIpServer *server = (*i);
            message = server->getBuffer();

            if (message != "")
            {
                pairActionpairInt command = CP.parseCommand(message); //returns (ActionType, (left, right))
                //cout << "parsed: " << command.first << " " << command.second.first << " " << command.second.second << endl;

                if (command.first == ENSLAVE)
                {
                    if (not server->enslaved())
                    {
                        MC.registerClient();
                        server->enslave(true);
                    }
                }
                else if (command.first == RELEASE)
                {
                    if (server->enslaved())
                    {
                        MC.unregisterClient();
                        server->enslave(false);
                    }
                }
                else if (command.first == STATUS)
                {
                    char msg[255];
                    msg[0] = 0;
                    MC.getStatusString(msg);
                    server->sendMsg(msg);
                }
                else
                {
                    // Execute command if the connection to the robot is available
                    if (server->enslaved())
                    {
                        if (MC.connected())
                        {
                            MC.handleCommand(command);
                        }
                        else
                        {
                            if (MC.error() != MotionController::INITIALIZING)
                            {
                                cerr << "[MotionController] No connection to robot available. Sending emergency\n" << flush;
                                server->sendEmergency();
                            }
                        }
                    }
                    else
                    {
                        cerr << "[MotionController] Client requests command while not enslaved, ignoring\n" << flush;
                    }
                }
            }
            if (server->sendTick())
            {
                double curTime = pythonTime();
                if (odo_time < curTime - 0.05)
                {
                    odo_time = curTime;
                    if (server->enslaved())
                    {
                        if (MC.error() == MotionController::NO_ERROR)
                        {
                            robot_was_working = true;
                            char msg[255];
                            msg[0] = 0;
                            MC.getOdometryString(msg);
                            server->sendMsg(msg);
                        }
                        else if (MC.error() != MotionController::INITIALIZING)
                        {
                            server->sendEmergency();
                            robot_was_working = false;
                        }
                    }
                }
            }

        }
        connection_lock.unlock();
        usleep(50000); //sleep 1/10 of a second
    }
    
    // Close all connections
    cout << "[MotionController] Server shutting down\n";
    sleep(1);
    connection_lock.lock();

    //First remove the actual object from memory to avoid memory leak.
    for (vector<TcpIpServer *>::iterator i = deletedConnections.begin(); i != deletedConnections.end(); ++i)
    {
        delete *i;
    }

    //Shutdown the rest of the active threads.
    for (vector<TcpIpServer *>::iterator i = connections.begin(); i != connections.end(); ++i)
    {
        (*i)->closeConnection();
        delete *i;
    }
    connection_lock.unlock();
    MC.stop();
    sleep(1);
    listener->stop();
    delete listener;

    return 0;
}

