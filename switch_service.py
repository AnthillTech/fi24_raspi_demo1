'''
Created on Aug 12, 2014

@summary: This module fully implements a simple functionality of a switch device. Depending on the command line parameters
it creates one or more virtual devices, each monitoring the state of a single GPIO pin in Raspberry Pi. 
@author: Piotr Orzechowski
@copyright: Anthill Technology
@license: GPL
@version: 0.2
@note: Early beta version
@todo: remove excessive debug prints
'''

import sys
import os
import getopt
from mewa.client import Connection
import time
import threading

from globalids import *




try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")



DEVICE_NAME_PREFIX = "RasPi_Switch-"
'''Name, which the device uses to connect to the channel'''

g_PinsToWatch = []
'''List of pin numbers of RasPi's port P1 to watch'''


g_MyDevices = []



class SwitchDevice(threading.Thread):
    
   
    mPinNo = -1
    '''Stores the number of RasPi's GPIO pin to watch'''
    mDeviceName = "" 
    '''Stores the device name (the name of the service instance)'''
    mConnection = Connection
    '''Connection object representing channel API'''
    mChannelPwd = ""
    '''Channel password'''
    mChannelName = ""
    '''Channel name'''
   
    def __init__(self, device_name, pin_no, fq_channel_name, channel_pwd):
        super(SwitchDevice,self).__init__()

        self.mPinNo = pin_no
        self.mDeviceName = device_name
        self.mChannelPwd = channel_pwd
        self.mChannelName = fq_channel_name
        
        #
        # Set up the RasPi inputs
        #        
        #GPIO.cleanup(pin_no)
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
        
        self.mConnection.connect(self.mChannelName,self.mDeviceName,self.mChannelPwd)

   
   
    
    def run(self):
        print "%s started - device %s, pin %s \n" % (self.getName(),self.mDeviceName,self.mPinNo)
        
        while True:
            GPIO.wait_for_edge(self.mPinNo, GPIO.BOTH)
            time.sleep(0.025)
            if GPIO.input(self.mPinNo):
                ev_id = URI_SWITCH_EV_SWITCHON
            else:
                ev_id = URI_SWITCH_EV_SWITCHOFF
            print "Sending event: ", ev_id
            self.mConnection.sendEvent(ev_id, "")
        
        
    def getDeviceName(self):
        return self.mDeviceName
        
    def getServiceTypes(self):
        return [URI_DISCOVERY,URI_SWITCH]
    
    '''API channel callbacks'''
    
    def onConnected (self):
        print "%s.onConnected" % (self.getDeviceName())
        
        
    def onDeviceJoined (self, dev_name):
        print "%s.onDeviceJoined: %s" % (self.getDeviceName(),dev_name)
    
    def onDeviceLeftChannel (self, dev_name):
        print "%s.onDeviceLeftChannel: %s" % (self.getDeviceName(),dev_name)
    
    def onDevicesEvent (self, devices_list):
        print "%s.onDevicesEvent: %s" % (self.getDeviceName(),devices_list)
    
    def onError (self, reason):
        print "%s.onError: %s" % (self.getDeviceName(), reason)
        print "Restarting connection in 5 seconds"
        time.sleep(5)
        self.mConnection.connect(self.mChannelName,self.mDeviceName,self.mChannelPwd)
        
    def onEvent (self, from_device, eventId, params):
        print "%s.onEvent: from=%s, msgId=%s" % (self.getDeviceName(), from_device, eventId)
        
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
       
       
    channel_name = ''
    channel_password = ''
    

    
    try:
        
        opts,args = getopt.getopt(sys.argv[1:],"c:p:i:")
        
    except getopt.GetoptError:
        print ("\nUsage: %s -c <channel_name> -p <channel_password> -i <pin_number>  { -i <pin_number> }   \n" % (os.path.basename(sys.argv[0])))
        print ("       channel_name ::= string")
        print ("               fully qualified channel name\n")
        print ("       channel_password ::= string")
        print ("               channel access password set by the channel owner\n")
        print ("       pin_number ::= int ")
        print ("               Number of the pin on Raspberry Pi port P1 which will be used")
        print ("               as input. More than one pin can be specified\n")
        sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-c':
            channel_name = arg            
        elif opt == "-p":
            channel_password = arg
        elif opt == "-i":
            try:
                pin_no = int(arg)
            except:
                print "pin number must be an integer"
                exit (2)
            g_PinsToWatch.append(pin_no)
                
                
    
    #
    # Start a few switch devices, each monitoring one input on RasPi 
    # 
    for i in g_PinsToWatch:
        devname = "%s%s" % (DEVICE_NAME_PREFIX,i)
        sthread = SwitchDevice(devname, i, channel_name, channel_password)
        sthread.start()
          

    


if __name__ == "__main__":
    main()
    
        
        
                      
        
    
    
    
    