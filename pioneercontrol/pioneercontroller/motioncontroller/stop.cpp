#include "MotionController.h"
#include <iostream>

using namespace std;

void MotionController::stop()
{
    if (d_running)
    {
        d_running = false;
        d_thread.join();
    }
}
