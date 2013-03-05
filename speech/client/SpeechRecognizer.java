package vcc;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

import edu.cmu.sphinx.frontend.util.Microphone;
import edu.cmu.sphinx.recognizer.Recognizer;
import edu.cmu.sphinx.result.Result;
import edu.cmu.sphinx.util.props.ConfigurationManager;
public class SpeechRecognizer { 
    
    SpeechClient speechclient;
    private ConfigurationManager cm;
    private Result result;
    
    public SpeechRecognizer(String[] args) throws Exception
    {
        cm = null;
        
        int port = 50025;
        if (args.length == 2)
        {
            String p = args[1];
            port = Integer.parseInt(p);
        }
        speechclient = new SpeechClient();
        if (speechclient.Connect("localhost", port))
            System.out.println("Connected ...");
        
        //default config
        System.out.println("[" + getDateTime() + "] initializing default recognizer... on port" + port);
        
        try {
            cm = new ConfigurationManager(Main.class.getResource("/" + args[0]));
        } catch (Exception e) {
            throw new Exception("Could not open xml file: " + "/" + args[0]); 
        }
        
        Recognizer recognizer = (Recognizer) cm.lookup("recognizer");
        recognizer.allocate();
        
        System.out.println("[" + getDateTime() + "] initializing microphone..");
        Microphone microphone = (Microphone) cm.lookup("microphone"); //same for all configs
        
        if (!microphone.startRecording()) {
            System.out.println("Cannot init microphone.");
            recognizer.deallocate();
            System.exit(1);
        }
        
        System.out.println("[" + getDateTime() + "] listening..");
        
        while (true) {
            result = recognizer.recognize();
            if (result != null) {
                String res = result.getBestFinalResultNoFiller();
                
                System.out.println("[" + getDateTime() + "] voice command: " + res);
                speechclient.sendSpeechCommand(res);
            } else {
                System.out.println("WHAT?\n");
            }
        }
    }
    
    private String getDateTime() {
        DateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
        Date date = new Date();
        return dateFormat.format(date);
    }
}
