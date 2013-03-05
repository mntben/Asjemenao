#include "commandparser.h"

#include <iostream>
#include <sstream>


pairActionpairInt CommandParser::parseCommand(std::string toParse)
{
    //commands like: `leftright 400 300', `xytheta 30 40 90', ...
    std::stringstream sstream;
    sstream << toParse;
    std::string command;
    sstream >> command;
    if (command == "enslave")
    {
        return pairActionpairInt(ENSLAVE, pairInt(0, 0));
    }
    else if (command == "release")
    {
        return pairActionpairInt(RELEASE, pairInt(0, 0));
    }
    else if (command == "status")
    {
        return pairActionpairInt(STATUS, pairInt(0, 0));
    }
    else if (command == "leftright")
    {
        int left(0), right(0);
        sstream >> left >> right;
        if(sstream.fail())
            return pairActionpairInt(NONE, pairInt(0, 0)); //left and right couldn't be read
        return pairActionpairInt(LEFTRIGHT, pairInt(left, right)); //everything is ok
    }
    else if (command == "forward")
    {
        int distance(0);
        sstream >> distance;
        if(sstream.fail())
            return pairActionpairInt(NONE, pairInt(0, 0)); //left and right couldn't be read
        return pairActionpairInt(FORWARD, pairInt(distance, 0)); //everything is ok    
    }
    else if (command == "turn")
    {
        std::cout << "turn!" << std::endl;
        int degrees(0);
        sstream >> degrees;
        if (sstream.fail())
            return pairActionpairInt(NONE, pairInt(0, 0)); //left and right couldn't be read
        return pairActionpairInt(TURN, pairInt(degrees, 0)); //everything is ok    
    }
    else if (command == "stop")
    {
        return pairActionpairInt(LEFTRIGHT, pairInt(0, 0));
    }
    else if (command == "options")
    {
    	std::cout << "options!" << std::endl;
		int option1(0), option2(0);
		sstream >> option1 >> option2;
		if (sstream.fail())
			return pairActionpairInt(NONE, pairInt(0, 0)); //options couldn't be read
        return pairActionpairInt(OPTIONS, pairInt(option1, option2));
    }
    return pairActionpairInt(NONE, pairInt(0, 0));
}
