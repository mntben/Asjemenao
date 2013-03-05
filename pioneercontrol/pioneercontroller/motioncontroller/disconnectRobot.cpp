#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::disconnectRobot(bool del)
{
    if (not d_connected)
        return;

    cout << "[MotionController] Disconnecting from robot\n";

    d_lock.lock();
    myRobot->stopRunning();
    if (del)
    {
        delete myRobot;
        myRobot = 0;
    }
    d_connected = false;
    d_lock.unlock();
}
