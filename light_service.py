'''
Created on Aug 12, 2014

@summary: This module fully implements a simple functionality of a light device. Depending on the command line parameters
it creates one or more virtual devices, each controlling the state of a single GPIO pin in Raspberry Pi. 
@author: Piotr Orzechowski
@copyright: Anthill Technology
@license: GPL
@version: 0.1
@note: Early beta version

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



DEVICE_NAME_PREFIX = "RasPi_Light-"
'''Name, which the device uses to connect to the channel'''

g_PinsToControl = []
'''List of pin numbers of RasPi's port P1 to control'''


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
        GPIO.setup(pin_no, GPIO.OUT) 
        
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
        print "%s started - using pin #%s \n" % (self.mDeviceName,self.mPinNo)
        
        while True:
            time.sleep(1)
        
        
    def getDeviceName(self):
        return self.mDeviceName
        
    def getServiceTypes(self):
        return [URI_DISCOVERY,URI_LIGHT]
    
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
        if eventId == URI_SWITCH_EV_SWITCHON:
            GPIO.output(self.mPinNo, not GPIO.input(self.mPinNo))
    
        
    def onMessage (self, from_device, msgId, params):
        print "%s.onMessage: from=%s, msgId=%s" % (self.getDeviceName(), from_device, msgId)
        try:
        
            if  msgId == URI_DISCOVERY_GETSERVICES:
            
                print "Sending: %s, %s, %s" % (from_device,URI_DISCOVERY_SERVICELIST,self.getServiceTypes()) 
                self.mConnection.sendMessage(from_device,URI_DISCOVERY_SERVICELIST,self.getServiceTypes())
  
            
            elif  msgId == URI_LIGHT_CMD_GETSTATE:
                if GPIO.input(self.mPinNo):
                    curstate="on"
                else:
                    curstate="off"
                
                print "Sending: %s, %s, %s" % (from_device,URI_LIGHT_RSP_CURSTATE,{"state":curstate}) 
                self.mConnection.sendMessage(from_device,URI_LIGHT_RSP_CURSTATE,{"state":curstate})
            
            elif  msgId == URI_LIGHT_CMD_ON:
                GPIO.output(self.mPinNo,1)
            
            elif  msgId == URI_LIGHT_CMD_OFF:
                GPIO.output(self.mPinNo,0)

            elif  msgId == URI_LIGHT_CMD_TOGGLE:
                GPIO.output(self.mPinNo,GPIO.input(self.mPinNo))

            
        except Exception, e:
            print "Exception", e
    

def main():
       
       
    channel_name = ''
    channel_password = ''
    

    
    try:
        
        opts,args = getopt.getopt(sys.argv[1:],"c:p:o:")
        
    except getopt.GetoptError:
        print ("\nUsage: %s -c <channel_name> -p <channel_password> -o <pin_number>  { -o <pin_number> }   \n" % (os.path.basename(sys.argv[0])))
        print ("       channel_name ::= string")
        print ("               fully qualified channel name\n")
        print ("       channel_password ::= string")
        print ("               channel access password set by the channel owner\n")
        print ("       pin_number ::= int ")
        print ("               Number of the pin on Raspberry Pi port P1 which will be used")
        print ("               as output. More than one pin can be specified\n")
        sys.exit(2)
    
    for opt,arg in opts:
        if opt == '-c':
            channel_name = arg            
        elif opt == "-p":
            channel_password = arg
        elif opt == "-o":
            try:
                pin_no = int(arg)
            except:
                print "pin number must be an integer"
                exit (2)
            g_PinsToControl.append(pin_no)
                
                
    
    #
    # Start a few switch devices, each monitoring one input on RasPi 
    # 
    for i in g_PinsToControl:
        devname = "%s%s" % (DEVICE_NAME_PREFIX,i)
        sthread = SwitchDevice(devname, i, channel_name, channel_password)
        sthread.start()
          

    


if __name__ == "__main__":
    main()
    
        
        
                      
        
    
    
    
    