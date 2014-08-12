'''
Created on Aug 12, 2014

@author: Piotr Orzechowski
@copyright: Anthill Technology
@license: GPL
@version: 0.1
@note: Early beta version
@todo: read RasPi GPIO pins to use from the command line (now they are hardcoded)
@todo: remove excessive debug prints
'''

import sys
import os
from mewa.client import Connection
import time
import threading

from globalids import *



try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")



DEVICE_NAME_PREFIX = "RasPi_Light_Switch"
'''Name, which the device uses to connect to the channel'''
PINS_TO_READ = [15,16]
'''List of pin numbers of RasPi's port P1 to watch'''


g_MyDevices = []



class SwitchDevice(threading.Thread):
    
   
    mPinNo = -1
    '''Stores the number of RasPi's GPIO pin to watch'''
    mDeviceName = "" 
    '''Stores the device name (the name of the service instance)'''
    mConnection = Connection
    '''Connection object representing channel API'''
    
   
    def __init__(self, device_name, pin_no, fq_channel_name, channel_pwd):
        super(SwitchDevice,self).__init__()

        self.mPinNo = pin_no
        self.mDeviceName = device_name
        
        #
        # Set up the RasPi inputs
        #        
        GPIO.cleanup(pin_no)
        GPIO.setup(pin_no, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        
        #
        # Instantiate connection object
        #
        self.mConnection = Connection("ws://channels.followit24.com/ws")
        #
        # Set-up callback functions
        #
        self.mConnection.onConnected = self.onConnected
        self.mConnection.onDeviceJoinedChannel = self.onDeviceJoined
        self.mConnection.onDeviceLeftChannel = self.onDeviceLeftChannel
        self.mConnection.onDevicesEvent = self.onDevicesEvent
        self.mConnection.onError = self.onError
        self.mConnection.onEvent = self.onEvent
        self.mConnection.onMessage = self.onMessage
        #
        # Open connection to channel server
        #
        self.mConnection.connect(fq_channel_name, device_name, channel_pwd)

   
   
    
    def run(self):
        print "%s started - device %s, pin %s \n" % (self.getName(),self.mDeviceName,self.mPinNo)
        
        while True:
            GPIO.wait_for_edge(self.mPinNo, GPIO.BOTH)
            time.sleep(0.05)
            if GPIO.input(self.mPinNo):
                ev_id = URI_SWITCH_EV_SWITCHON
            else:
                ev_id = URI_SWITCH_EV_SWITCHOFF
            print "Sending event: ", ev_id
            self.mConnection.sendEvent(ev_id, "")
            time.sleep(1)
        
    def getDeviceName(self):
        return self.mDeviceName
        
    def getServiceTypes(self):
        return [URI_DISCOVERY,URI_SWITCH]
    
    '''API channel callbacks'''
    
    def onConnected (self):
        print "%s: Connected to channel" % (self.getDeviceName())
        pass
        
    def onDeviceJoined (self, dev_name):
        print "onDeviceJoined:",dev_name
    
    def onDeviceLeftChannel (self, dev_name):
        print "onDeviceLeftChannel:",dev_name
    
    def onDevicesEvent (self, devices_list):
        print "onDevicesEvent:",devices_list
    
    def onError (self, reason):
        print "onError:",reason
        
    def onEvent (self, from_device, eventId, params):
        print "onEvent", from_device, eventId, params
        
    def onMessage (self, from_device, msgId, params):
        print "%s.onMessage: from=%s, msgId=%s" % (self.getDeviceName(), from_device, msgId)
        #
        # Intercept calls to mandatory service com.followit24.service.discovery  
        #
        if  msgId == URI_DISCOVERY_GETSERVICES:
            try:
                print "Sending: %s, %s, %s" % (from_device,URI_DISCOVERY_SERVICELIST,self.getServiceTypes()) 
                self.mConnection.sendMessage(from_device,URI_DISCOVERY_SERVICELIST,self.getServiceTypes())
             
            except Exception, e:
                print "Exception", e
        
            pass
        elif  msgId == URI_SWITCH_GETSTATE:
            try:
                if GPIO.input(self.mPinNo):
                    curstate="on"
                else:
                    curstate="off"
                print "Sending: %s, %s, %s" % (from_device,URI_SWITCH_CURSTATE,curstate) 
                self.mConnection.sendMessage(from_device,URI_SWITCH_CURSTATE,curstate)
             
            except Exception, e:
                print "Exception", e
        
            pass

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
    # Start a few switch devices, each monitoring one input on RasPi 
    # 
    for i in PINS_TO_READ:
        devname = "%s%s" % (DEVICE_NAME_PREFIX,i)
        sthread = SwitchDevice(devname, i, channel_name, channel_password)
        sthread.start()
          

    


if __name__ == "__main__":
    main()
    
        
        
                      
        
    
    
    
    