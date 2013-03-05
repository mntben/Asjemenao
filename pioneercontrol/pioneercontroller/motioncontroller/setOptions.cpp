#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::setOptions(int option1, int option2)
{
    if (not d_connected)
    {
        cerr << "[MotionController] Not connected to robot, so not sending command\n";
        return;
    }
    myRobot->lock();

    switch(option1)
    {
    	case 0:
    		cout << "[MotionController] Set Rotation Velocity Max Speed to " << option2 << endl;
    		myRobot->setRotVelMax(option2);
			break;
    	case 1:
    		cout << "[MotionController] Set Rotation Acceleration to " << option2 << endl;
			myRobot->setRotAccel(option2);
    		break;
    	case 2:
    		cout << "[MotionController] Set Rotation Deceleration to " << option2 << endl;
			myRobot->setRotDecel(option2);
			break;
    	case 3:
    		cout << "[MotionController] Set Translational Acceleration to " << option2 << endl;
    		myRobot->setTransAccel(option2);
    		break;
    	case 4:
    		cout << "[MotionController] Set Translational Deceleration to " << option2 << endl;
    		myRobot->setTransDecel(option2);
    		break;
    }

    myRobot->unlock();
}
