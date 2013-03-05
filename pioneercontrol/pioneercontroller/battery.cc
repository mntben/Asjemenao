#include <iostream>
#include <cstring>
#include <cstdlib>
#include <climits>
#include <Aria.h>

using namespace std;

int main()
{
    int nargs = 0;
    char *args = 0;
    ArLog::init(ArLog::None, ArLog::Terse, "", false, false, false);
    ArSimpleConnector con(&nargs, &args);
    ArRobot myRobot;
    if (con.connectRobot(&myRobot))
    {
        cout << "Pioneer battery level: " << myRobot.getBatteryVoltage() << "\n";
        return 0;
    }
    return 1;
}
