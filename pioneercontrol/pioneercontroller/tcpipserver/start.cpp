#include "server.h"
#include <iostream>

void TcpIpServer::start()
{
	bool thread = false;
    d_running = true;
    while (not thread)
		try
    	{
			d_thread = std::thread(&TcpIpServer::runner, this);
			thread = true;
		}
		catch (...)
		{
			std::cout << "starting thread failes\n";
		}

}

