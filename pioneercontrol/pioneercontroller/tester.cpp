#include <cppunit/Test.h>
#include <cppunit/TestFixture.h>
#include <cppunit/TestSuite.h>
#include <cppunit/TestAssert.h>
#include <cppunit/TestCaller.h>
#include "commandparser/commandparser.h"
#include "tcpipserver/server.h"
#include <iostream>
#include <string>
#include <unistd.h>
#include "types.h"

using namespace std;

class PioneerControlTest : public CppUnit::TestFixture  {
    private:

    public:
        void setUp()
        {

        }

        void tearDown() 
        {

        }

        void testParser()
        {
            string toParse[] = {"leftright 100 100", "bullshit", "leftright 100 -100", "stop", "stop bullshit", "leftright", "leftright bull shit", "forward 100", "forward", "turn -50"};
            pairActionpairInt expected[] = 
            {
                pairActionpairInt(LEFTRIGHT, pairInt(100, 100)),
                pairActionpairInt(NONE, pairInt(0, 0)),
                pairActionpairInt(LEFTRIGHT, pairInt(100, -100)),
                pairActionpairInt(LEFTRIGHT, pairInt(0, 0)),
                pairActionpairInt(LEFTRIGHT, pairInt(0, 0)),
                pairActionpairInt(NONE, pairInt(0, 0)),
                pairActionpairInt(NONE, pairInt(0, 0)),
                pairActionpairInt(FORWARD, pairInt(100, 0)),
                pairActionpairInt(NONE, pairInt(0, 0)),
                pairActionpairInt(TURN, pairInt(-50, 0))
            };
            size_t nTests = 10;
            CommandParser CP;
            for(size_t i = 0; i < nTests; i++)
            {
              pairActionpairInt result;
              result = CP.parseCommand(toParse[i]);
              //cout << toParse[i] << " - " << result.first << " " << result.second.first << " " << result.second.second << endl;
              CPPUNIT_ASSERT( result == expected[i] );
            }
        }
  
        void testReceiveMsg()
        {
            TcpIpServer server(5550);
            string message;
            string systemCommand = "";
            //make sure the server is waiting for a connection by first sleeping a little bit
            //write the messages (with endlines), 
            //pipe the message to telnet, redirecting all output of telnet so it doesn't end up in the konsole
            systemCommand.append("(sleep 1;(echo 'message1' && echo 'message2') | telnet localhost 5550 >/dev/null 2>&1)&");
            system(systemCommand.c_str()); //execute the system command
            server.acceptConnection();
            while( (message = server.receiveMsg()) == "")
            {
                sleep(1);
            }
            CPPUNIT_ASSERT( string(message).substr(0,8) == string("message1") );
            
            while( (message = server.receiveMsg()) == "")
            {
                sleep(1);
            }
            CPPUNIT_ASSERT( string(message).substr(0,8) == string("message2") );
        }

    public:
        static CppUnit::Test *suite()
        {
            CppUnit::TestSuite *suiteOfTests = new CppUnit::TestSuite( "PioneerControlTest" );
            suiteOfTests->addTest( new CppUnit::TestCaller<PioneerControlTest> ( 
                                           "testParser", 
                                           &PioneerControlTest::testParser ) );
            suiteOfTests->addTest( new CppUnit::TestCaller<PioneerControlTest> ( 
                                           "testReceiveMsg", 
                                           &PioneerControlTest::testReceiveMsg ) );
            return suiteOfTests;
        }
};

#include <cppunit/ui/text/TestRunner.h>

int main( int argc, char **argv)
{
    CppUnit::TextUi::TestRunner runner;
    runner.addTest( PioneerControlTest::suite() );
    runner.run();
    return 0;
}

