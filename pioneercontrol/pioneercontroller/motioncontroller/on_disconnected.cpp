#include "MotionController.h"

// lost connection, so just exit
void MotionController::on_disconnected(void)
{
    printf("[MotionController] Robot connection handler: Lost connection.\n");
    d_error = CONNECTION_LOST;
    disconnectRobot(false);
}
