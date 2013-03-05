#include <iostream>
#include <sstream>
#include "commandparser.h"
using namespace std;

int main()
{
  
  CommandParser CP;
  pairActionpairInt result = CP.parseCommand("leftright 400 1000");
  cout << result.first << " " << result.second.first << " " << result.second.second << endl;
  result = CP.parseCommand("stop");
  cout << result.first << " " << result.second.first << " " << result.second.second << endl;
  result = CP.parseCommand("onzin 34 356");
  cout << result.first << " " << result.second.first << " " << result.second.second << endl;
  
  
  return 0;
}
