#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::setSpeeds(int leftSpeed, int rightSpeed)
{
    if (not d_connected)
    {
        cerr << "[MotionController] Not connected to robot, so not sending command\n";
        return;
    }
    myRobot->lock();
    cout << "[MotionController] Set left/right speeds to " << leftSpeed << ", " << rightSpeed << endl;
    myRobot->setVel2(leftSpeed, rightSpeed);
    myRobot->unlock();
}
