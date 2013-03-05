#include "MotionController.h"
#include <iostream>


MotionController::MotionController()
:
    myRobot(0),
    d_connected(false),
    d_nClients(0),
    d_running(false),
    d_myConnectedCB(this, &MotionController::on_connected),  
    d_myConnFailCB(this, &MotionController::on_connFail),
    d_myDisconnectedCB(this, &MotionController::on_disconnected)
{
    d_doTimeOut = false;  
    d_maxIdleTime = 0.5;
    // Do not let Aria handle signals, as the main program will take care of that
    Aria::init(Aria::SIGHANDLE_NONE);
}
