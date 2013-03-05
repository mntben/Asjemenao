#ifndef INCL_TYPES_H
#define INCL_TYPES_H
#include <exception>
enum ActionType {NONE = 0, LEFTRIGHT, FORWARD, TURN, ENSLAVE, RELEASE, STATUS, OPTIONS};

typedef std::pair<ActionType, std::pair<int, int> > pairActionpairInt;
typedef std::pair<int, int> pairInt;

#endif
