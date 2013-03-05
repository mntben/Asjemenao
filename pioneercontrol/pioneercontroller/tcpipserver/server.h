#ifndef INCL_SERVER_H
#define INCL_SERVER_H

#include <sys/socket.h>       /*  socket definitions        */
#include <sys/types.h>        /*  socket types              */
#include <arpa/inet.h>        /*  inet (3) funtions         */
#include <unistd.h>           /*  misc. UNIX functions      */

//#include "helper.h"           /*  our own helper functions  */
#include <thread>
#include <mutex>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <vector>


/*  Global constants  */
#define ECHO_PORT          (2002)
#define MAX_LINE           (1024)
#define LISTENQ        (1024)   /*  Backlog for listen()   */

class TcpIpServer
{
    private:
        size_t d_port;
        int    d_list_s; //listen socket
        int    d_conn_s; //socket connection
      
        enum {ST_SEND_IDLE, ST_SEND_BUSY} sender_state;
        int bytes_remaining;
        int msg_size;
        char send_buffer[255];
        //Not used anywhere  std::vector<TcpIpServer *> d_connections;
        bool d_running;
        bool d_enslaved;
        bool d_connection_closed;
        bool d_listening;
        std::string d_buffer;
        std::mutex d_lock;
        std::thread d_thread;
  
    public:
        TcpIpServer(size_t);
        TcpIpServer(size_t, int socket);
        ~TcpIpServer();
          
        bool acceptConnection();
        void closeConnection();
        std::string receiveMsg();

        int socket() const;

        bool enslaved() const;
        bool listening() const;
        void enslave(bool enslave = true);
          
        /**
         * Puts the specified string in the buffer to be send (non-blocking).
         * This can function can only be called once the sendTick function returns true.
         */
        void sendMsg(std::string msg);
        
        /**
         * This will send the emergency signal to the brain
         */
        void sendEmergency();
  
        /**
         * Sends the remaining bytes (if any) for the previously specified message (with sendMsg(...)).
         * Call this function as often as posssible.
         */
        bool sendTick();

        // Threading functions
        std::string getBuffer(); // Returns commands received and clears buffer
        void start();            // Starts thread
        void stop();             // Stops thread
        //static void *runner(void *arg); // Connection handling thread
        void runner(); // Connection handling thread
};

inline int TcpIpServer::socket() const
{
    return d_conn_s;
}

inline bool TcpIpServer::enslaved() const
{
    return d_enslaved;
}

inline void TcpIpServer::enslave(bool enslave)
{
    d_lock.lock();
    d_enslaved = enslave;
    d_lock.unlock();
}

inline bool TcpIpServer::listening() const
{
    return d_listening;
}
#endif
