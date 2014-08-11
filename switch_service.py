import sys
import os
from mewa.client import Connection
from mewa.client import Protocol
import time
import json
import threading



try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")



DEVICE_NAME = "RasPi Light Switch"
'''Name, which the device uses to connect to the channel'''
SERVICE_NAME_PREFIX = "GPIO-" 
'''Prefix for naming the services exposed by this device''' 
SWITCH_SERVICE_URI = "com.followit24.service.switch"
'''URI of the service '''
PINS_TO_READ = [15,16]
'''List of pin numbers of RasPi's port P1 to watch'''



g_Connection = Connection("ws://channels.followit24.com/ws")
g_MyServices = {}



class SwitchService(threading.Thread):
    
   
    mPinNo = -1
    '''Stores the number of RasPi's GPIO pin to watch'''
    mServiceName = "" 
    '''Stores the service name (the name of the service instance)'''
   
    def __init__(self, service_name, pin_no):
        super(SwitchService,self).__init__()

        self.mPinNo = pin_no
        self.mServiceName = service_name
        
        GPIO.cleanup(pin_no)
        GPIO.setup(pin_no, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

   
    
    def run(self):
        print "%s started - service %s, pin %s \n" % (self.getName(),self.mServiceName,self.mPinNo)
        while True:
            GPIO.wait_for_edge(self.mPinNo, GPIO.BOTH)
            time.sleep(0.05)
            if GPIO.input(self.mPinNo):
                ev_id = "%s.%s" % (self.getServiceName(),"SwitchOn")
            else:
                ev_id = "%s.%s" % (self.getServiceName(),"SwitchOff")
            print "Sending event: ", ev_id
            g_Connection.sendEvent(ev_id, "")
        
                
        
    def getServiceName(self):
        return self.mServiceName
        
    def getServiceURI(self):
        return SWITCH_SERVICE_URI
    
       
        
        


def onConnected():
    print "onConnected: connected to channel successfully..."
    
def onDeviceJoined (dev_name):
    print "onDeviceJoined:",dev_name

def onDeviceLeftChannel (dev_name):
    print "onDeviceLeftChannel:",dev_name

def onDevicesEvent (devices_list):
    print "onDevicesEvent:",devices_list

def onError (reason):
    print "onError:",reason
    
def onEvent (from_device, eventId, params):
    print "onEvent", from_device, eventId, params
    
    
def onMessage (from_device, msgId, params):
    print "onMessage:", from_device, msgId, params
    #
    # Intercept calls to mandatory service com.followit24.service.discovery  
    #
    if  "discovery.GetServices" == msgId.strip():
        try:
            slist = []
            for sname in  g_MyServices.iterkeys():
                slist.append({"name":sname,"type":g_MyServices[sname]})
            print "Sending: %s, %s, %s" % (from_device,"discovery.ServiceList",slist) 
            g_Connection.sendMessage(from_device,"discovery.ServiceList",slist)
        
        except Exception, e:
            print "Exception", e
    
    


def main():
    if len(sys.argv) != 3:
        print ("\nUsage: %s  <channel_name> <channel_password>\n" % (os.path.basename(sys.argv[0])))
        print ("       channel_name ::= string")
        print ("               fully qualified channel name\n")
        print ("       channel_password ::= string")
        print ("               channel access password set by the channel owner\n")
        sys.exit(1)
    else:
        channel_name=sys.argv[1]
        channel_password=sys.argv[2]  
    
       
  
    #
    # Start a few switch services, each monitoring different 
    # 
    for i in PINS_TO_READ:
        sname = "%s%s" % (SERVICE_NAME_PREFIX,i)
        sthread = SwitchService(sname, i)
        g_MyServices[sname] = sthread.getServiceURI()
        sthread.start()
  
  
               
    #
    # Set-up callback functions
    #
    
    g_Connection.onConnected = onConnected
    g_Connection.onDeviceJoinedChannel = onDeviceJoined
    g_Connection.onDeviceLeftChannel = onDeviceLeftChannel
    g_Connection.onDevicesEvent = onDevicesEvent
    g_Connection.onError = onError
    g_Connection.onEvent = onEvent
    g_Connection.onMessage = onMessage
   
    #
    # Connect to channel
    #     Note that the connect method of the g_Connection object starts its own thread   
    #     which executes until the g_Connection is closed
    #     Therefore main function may terminate immediately  
    g_Connection.connect(channel_name, DEVICE_NAME, channel_password)                
      


if __name__ == "__main__":
    main()
    
        
        
                      
        
    
    
    
    