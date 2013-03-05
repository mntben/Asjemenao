#include "MotionController.h"
#include <iostream>
#include <ctime>

using namespace std;

void MotionController::runner()
{
    cout << "[MotionController] Robot control thread started\n";
    //MotionController *obj = reinterpret_cast<MotionController *>(arg);
    while (d_running)
    {
    	d_lock.lock();
        bool active = d_nClients > 0;
        bool connected = d_connected;
        if (not connected and (myRobot != 0))
        {
            delete myRobot;
            myRobot = 0;
        }
        d_lock.unlock();

        if (connected)
        {
            timespec currentTime;
            clock_gettime(CLOCK_REALTIME, &currentTime);
            float elapsedTime = tdif(d_receivedTime, currentTime);

            if ((elapsedTime > d_maxIdleTime) && d_doTimeOut)
                setSpeeds(0, 0); // stop when we haven't received a command for too long
        }

        if (active)
        {
            if (not connected)
            {
                usleep(999999);
                cout << "[MotionController] Connecting to robot...\n";
                connected = connectRobot();
            }
            if (not connected)
                continue;
        }
        else
        {
            // Not active; so not trying to connect and so no error state
            d_error = MotionController::NO_ERROR;
            if (connected)
            {
                cout << "[MotionController] No clients active, disconnecting robot\n";
                disconnectRobot();
            }
        }
        usleep(100000);
    }
    disconnectRobot();
    cout << "[MotionController] Robot control thread ended\n";
}
