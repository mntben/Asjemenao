#include "MotionController.h"

MotionController::~MotionController()
{
    if (connected())
    {
        disconnectRobot();
        stop();
    }
    Aria::shutdown();
}
