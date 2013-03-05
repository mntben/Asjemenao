#include "MotionController.h"
#include <iostream>
#include <sstream>
#include <cstring>

using namespace std;

void MotionController::getStatusString(char * msg)
{
    ostringstream out;
    d_lock.lock();
    if (connected())
    {
        out << "Connected: yes" << endl;
        myRobot->lock();
        out << "X: " << myRobot->getX() << endl
            << "Y: " << myRobot->getY() << endl
            << "Theta: " << myRobot->getTh() << endl
            << "Battery: " << myRobot->getBatteryVoltage() << endl;
        myRobot->unlock();
    }
    else
    {
        out << "Connected: no" << endl;
    }
    if (d_nClients > 0 && d_error != NO_ERROR && d_error != INITIALIZING)
        out << "Emergency: yes" << endl;
    else
        out << "Emergency: no" << endl;
        
    out << "Connections: " << d_nClients << endl;
    d_lock.unlock();

    char const *buf = out.str().c_str();
    strcpy(msg, buf);
}
