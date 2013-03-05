#include "MotionController.h"

// set error status if the connection failed
void MotionController::on_connFail(void)
{
    printf("[MotionController] Robot connection handler: Failed to connect.\n");

    d_error = CONNECTION_FAILED;
    disconnectRobot();
}
