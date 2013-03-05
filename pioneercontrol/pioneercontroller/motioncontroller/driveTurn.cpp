#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::driveTurn(int angle)
{
    if (not d_connected)
    {
        cerr << "[MotionController] Not connected to robot, so not sending command\n";
        return;
    }
    cout << "[MotionController] Setting Delta Heading to angle " << angle << endl;
    myRobot->setDeltaHeading(angle);
    myRobot->unlock();
}
