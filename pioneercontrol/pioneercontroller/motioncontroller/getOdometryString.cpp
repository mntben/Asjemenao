#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::getOdometryString(char * msg)
{
	d_lock.lock();
    if (connected())
    {
        myRobot->lock();
        sprintf(msg, "%f %f %f %f\n", myRobot->getX(), myRobot->getY(), myRobot->getTh(), myRobot->getBatteryVoltage());
        myRobot->unlock();
    }
    d_lock.unlock();
}
