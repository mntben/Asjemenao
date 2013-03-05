#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::driveForward(int distance)
{
    if (not d_connected)
    {
        cerr << "[MotionController] Not connected to robot, so not sending command\n";
        return;
    }
    myRobot->lock();
    cout << "[MotionController] Sending command to move " << distance << " at speed 200\n";
    myRobot->setTransVelMax(200);
    myRobot->move(distance);
    myRobot->unlock();
}
