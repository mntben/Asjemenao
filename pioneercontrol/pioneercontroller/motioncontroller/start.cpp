#include "MotionController.h"
#include <iostream>

using namespace std;

bool MotionController::start()
{
    //if (d_thread == 0)
    //{
		bool thread = false;
        d_running = true;
        while (not thread)
			try
        	{
				d_thread = std::thread(&MotionController::runner, this);
				thread = true;
			}
			catch (...)
			{
				cout << "starting thread failes\n";
			}
    //}

    return true;
}
