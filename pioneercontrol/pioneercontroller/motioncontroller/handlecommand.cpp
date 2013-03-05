#include "MotionController.h"

#include <ctime>
#include <unistd.h>
#include <iostream>

using namespace std;

float tdif(timespec t1, timespec t2)
{
    /* Returns the positive difference between t2 and t2, in seconds, with nanosecond precision */
    float secdif = (t2.tv_sec - t1.tv_sec);
    float nsecdif = (t2.tv_nsec - t1.tv_nsec);
    float totaldif = secdif + nsecdif/1e9;
    float absdif = totaldif > 0 ? totaldif : -totaldif;
    return absdif;
}

void MotionController::handleCommand(pairActionpairInt command)
{
    switch(command.first)
    {
        case LEFTRIGHT:
            setSpeeds(command.second.first, command.second.second); //set the speeds to the (left, right) values
            clock_gettime(CLOCK_REALTIME, &d_receivedTime);
            d_doTimeOut = true;
            break;
        case FORWARD:
            driveForward(command.second.first);
            clock_gettime(CLOCK_REALTIME, &d_receivedTime);
            d_doTimeOut = false;
            break;
        case TURN:
            driveTurn(command.second.first);
            clock_gettime(CLOCK_REALTIME, &d_receivedTime);
            d_doTimeOut = false;
            break;
        case OPTIONS:
        	setOptions(command.second.first, command.second.second);
        	clock_gettime(CLOCK_REALTIME, &d_receivedTime);
			d_doTimeOut = false;
        case NONE: //no (correct) action received //falling through
        default:   //or any other value
          timespec currentTime;
          clock_gettime(CLOCK_REALTIME, &currentTime);
          float elapsedTime = tdif(d_receivedTime, currentTime);

          if ((elapsedTime > d_maxIdleTime) && d_doTimeOut)
              setSpeeds(0, 0); // stop when we haven't received a command for too long
          
    }
}
