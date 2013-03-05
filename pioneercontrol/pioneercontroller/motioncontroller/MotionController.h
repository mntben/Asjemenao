#ifndef INCL_MOTIONCONTROLLER_H
#define INCL_MOTIONCONTROLLER_H

#include <thread>
#include <mutex>
#include <string>
#include <strings.h> //for Aria
#include <cstring>
#include <climits> //for Aria
#include <cstdlib> //for Aria
#include <vector>
#include <Aria.h>
#include "../types.h"



float tdif(timespec t1, timespec t2);

class MotionController {
    public:
        enum ERROR_STATE
        {
          NO_ERROR,
          CONNECTION_LOST,
          CONNECTION_FAILED,
          INITIALIZING
        };
  
    private:
        // robot pointer
        ArRobot *myRobot;
        ArRobot *tmpRobot;
        timespec d_receivedTime;
        double d_maxIdleTime;
        bool d_doTimeOut; //whether the robot should time out if not receives commands for d_maxIdleTime
        ERROR_STATE d_error;
        bool d_connected;
        int d_nClients;
        bool d_running;
        std::mutex d_lock;
        std::thread d_thread;

    protected:
        // the functor callbacks
        ArFunctorC<MotionController> d_myConnectedCB;
        ArFunctorC<MotionController> d_myConnFailCB;
        ArFunctorC<MotionController> d_myDisconnectedCB;
    
    public:
        MotionController();
        ~MotionController();

        bool connectRobot(); // Connect to the robot
        void disconnectRobot(bool del = true); // Disconnect from the robot

        bool connected() const; // Returns whether or not there is an active connectiona to the robot

        void registerClient(); // Increase the connection counter
        void unregisterClient(); // Decrease the connection counter
        size_t numClients() const; // Get the number of connected clients
    
        void driveForward(int); //move in millimeters
        void driveTurn(int);    //turn in degrees (??)
        void setSpeeds(int, int); //wheel speeds in mm/s
        void setOptions(int, int); //Options to control velocity and acceleration of rotation and translation movement.

        // to be called if the connection was made
        void on_connected(void);
        // to call if the connection failed
        void on_connFail(void);
        // to be called if the connection was lost
        void on_disconnected(void);
        //handle a command
        void handleCommand(pairActionpairInt);
        ERROR_STATE error() const;

        /**
        * Returns a string representation of the X, Y postion, angle and battery voltage level.
        * WARNING: Make sure the provided message buffer is at least 255 Bytes long.
        */
        void getOdometryString(char * msg);
        void getStatusString(char *msg);

        bool start();   // Starts the robot control thread
        void stop();    // Stops the robot control thread
        void runner();   // The robot control thread
};

inline MotionController::ERROR_STATE MotionController::error() const
{
    return d_error;
}

inline bool MotionController::connected() const
{
    return d_connected;
}

inline void MotionController::registerClient()
{
    d_lock.lock();
    ++d_nClients;
    d_lock.unlock();
}

inline void MotionController::unregisterClient()
{
	d_lock.lock();
    if (d_nClients > 0)
        --d_nClients;
    d_lock.unlock();
}

inline size_t MotionController::numClients() const
{
    return d_nClients;
}
#endif
