#put here all the objects that you want to be generated that DO NOT CONTAIN A MAIN() FUNCTION
COMMONOBJECTS = commandparser/commandparser1.o commandparser/destructor.o commandparser/parsecommand.o tcpipserver/destructor.o tcpipserver/receivemsg.o tcpipserver/acceptconnection.o tcpipserver/closeConnection.o tcpipserver/server1.o tcpipserver/server2.o tcpipserver/getBuffer.o tcpipserver/runner.o tcpipserver/start.o tcpipserver/stop.o motioncontroller/destructor.o motioncontroller/on_connFail.o motioncontroller/setSpeeds.o motioncontroller/setOptions.o motioncontroller/MotionController1.o motioncontroller/on_connected.o motioncontroller/on_disconnected.o motioncontroller/handlecommand.o motioncontroller/driveTurn.o motioncontroller/driveForward.o tcpipserver/sendmsg.o tcpipserver/sendtick.o tcpipserver/sendemergency.o motioncontroller/getOdometryString.o motioncontroller/connectRobot.o motioncontroller/disconnectRobot.o motioncontroller/runner.o motioncontroller/start.o motioncontroller/stop.o motioncontroller/getStatusString.o functions.o

#put here all header files that objects (might) be dependent upon
HEADERS = commandparser/commandparser.h tcpipserver/server.h motioncontroller/MotionController.h types.h

#For the different binaries to be generated
MAINOBJECTS = main.o $(COMMONOBJECTS)
TESTOBJECTS = tester.o $(COMMONOBJECTS)

# Find the correct location for Aria. Prefer the one in the Robotica SDK as it
# is more up to date
ARIADIR_1=/home/student/vakken/Robotica/sdk/Aria
ARIADIR_2=/usr/local/Aria
ARIADIR=$(shell test -d $(ARIADIR_1) && echo $(ARIADIR_1) )
ifeq ("$(ARIADIR)","")
	ARIADIR=$(shell test -d $(ARIADIR_2) && echo $(ARIADIR_2) )
endif

INCLUDES = -I$(ARIADIR)/include -L$(ARIADIR)/lib -Llib

LIBRARIES = -lAria -pthread -ldl -lrt -lcppunit

all: motionController motionControllerTest battery

motionController: $(MAINOBJECTS)  $(HEADERS)
	g++ -Wall --std=c++0x  -O2 $(INCLUDES) -o motionController $(MAINOBJECTS) $(LIBRARIES)
	 
motionControllerTest: $(TESTOBJECTS)  $(HEADERS)
	g++ -Wall --std=c++0x  -O2 $(INCLUDES) -o motionControllerTest $(TESTOBJECTS) $(LIBRARIES) -lcppunit

battery: battery.cc
	g++ -Wall --std=c++0x  -O2 $(INCLUDES) -o battery battery.cc $(LIBRARIES)
	 
%.o: %.cpp $(HEADERS)
	g++ -Wall --std=c++0x  -O2 $(INCLUDES) -pthread -c $< -o $@

clean:
	find . -name '*.o' -print0 | xargs -0 rm
	rm motionController
	rm motionControllerTest
	
.PHONY: clean all
