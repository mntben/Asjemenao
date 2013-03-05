#ifndef __INCLUDED_MOTION_MAIN_H_
#define __INCLUDED_MOTION_MAIN_H_

#include <pthread.h>
#include <thread>
#include <mutex>
#include <vector>
#include "motioncontroller/MotionController.h"
#include "tcpipserver/server.h"

extern std::vector<TcpIpServer *> connections;
extern std::vector<TcpIpServer *> deletedConnections;
//extern pthread_mutex_t connection_lock;
extern std::mutex connection_lock;
extern bool server_running;
extern MotionController MC;

void accepted_connection(int s);
void closed_connection(int s);
void shutdown();

#endif
