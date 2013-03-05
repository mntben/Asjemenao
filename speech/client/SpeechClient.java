package vcc;

import java.io.*;
import java.net.Socket;

public class SpeechClient {
    
    private Socket socket;
    private BufferedWriter os;
    private BufferedReader is;
    
    public boolean Connect(String host, int port) {
        try {
                socket = new Socket(host, port);
                socket.setKeepAlive(true);
                System.out.println(socket);
                os = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                return true;
            } 
        catch (Exception e) {
            System.err.println("Could not connect: " + e);
        }
        return false;
     }
    
    public void sendSpeechCommand(String command) {
        try {
                os.write(command);
                os.flush();
                System.out.println("Sent command: " + command);
                //System.out.println("Answer: " + is.readLine());
            } 
        catch (Exception e) {
        }
    }
}
