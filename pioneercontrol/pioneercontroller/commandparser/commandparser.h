#ifndef INCL_COMMANDPARSER_H
#define INCL_COMMANDPARSER_H

#include <string>
#include <vector>
#include "../types.h"


class CommandParser {
    public:
        CommandParser();
        ~CommandParser();
        pairActionpairInt parseCommand(std::string);
};


#endif
