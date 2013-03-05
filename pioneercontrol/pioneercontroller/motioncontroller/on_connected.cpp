#include "MotionController.h"

// turn on motors, and off sonar, and off amigobot sounds, when connected
void MotionController::on_connected(void)
{
    printf("[MotionController] Robot connection handler: Connected\n");
    d_error = NO_ERROR;
    if (tmpRobot != 0)
    {
        tmpRobot->comInt(ArCommands::SONAR, 0);
        tmpRobot->comInt(ArCommands::ENABLE, 1);
        tmpRobot->comInt(ArCommands::SOUNDTOG, 0);
    }
}
