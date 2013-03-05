#include "MotionController.h"
#include <iostream>
#include <fstream>
using namespace std;

bool MotionController::connectRobot()
{
    if (d_connected)
        return true;

    if (d_error == NO_ERROR)
    {
        d_error = INITIALIZING;
    }
    //int nargs = 0;
    //char *args = 0;
    
    
    
    
    ArArgumentBuilder *args;
    args = new ArArgumentBuilder();
    args->add("-rp"); //pass robot's serial port to Aria
    args->add("/dev/ttyUSB0");
    args->add("-rb");
    args->add("9600");

    //ArSimpleConnector con(&nargs,&args);
    ArSimpleConnector con(args);
    
    tmpRobot = new ArRobot;
    tmpRobot->addConnectCB(&d_myConnectedCB, ArListPos::FIRST);
    tmpRobot->addFailedConnectCB(&d_myConnFailCB, ArListPos::FIRST);
    tmpRobot->addDisconnectNormallyCB(&d_myDisconnectedCB, ArListPos::FIRST);
    tmpRobot->addDisconnectOnErrorCB(&d_myDisconnectedCB, ArListPos::FIRST);
    tmpRobot->setConnectionTimeoutTime(100);
    /*tmpRobot->setRotAccel(2);
    tmpRobot->setRotDecel(2);
    tmpRobot->setTransAccel(5);
    tmpRobot->setTransDecel(5);
    tmpRobot->setRotVel(5);*/
    cout << "[MotionController] Connecting to robot\n";
    if (!con.connectRobot(tmpRobot))
    {
        ArLog::log(ArLog::Normal, "[MotionController] Could not connect to the robot.");
        d_lock.lock();
        d_error = CONNECTION_FAILED;
        d_lock.unlock();
        delete tmpRobot;
        tmpRobot = 0;
        return false;
    }

    d_lock.lock();
  
    cout << "[MotionController] Connected\n";
    d_error = NO_ERROR;
    d_connected = true;
    myRobot = tmpRobot;
    tmpRobot = 0;
  
    // Run the robot processing cycle in its own thread. Note that after starting this
    // thread, we must lock and unlock the ArRobot object before and after
    // accessing it.
    myRobot->runAsync(false);
    
    clock_gettime(CLOCK_REALTIME, &d_receivedTime); //initialize d_receivedTime (time we last received a non-empty message)
    d_lock.unlock();
    return true;
}
