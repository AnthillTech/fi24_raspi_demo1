# fi24_raspi_demo1

This projects serves as a demonstration of how followit24.com channels can be used to easily implement a distributed *hallway switch* functionality using one or more Raspberry Pi
The functionality of this demonstration system is rather simple:  

- you start the Light Switch service on each Raspberry Pi that you want to work in the network. 
- command line options determine which GPIO pins are outputs (light) or inputs (switch)
- as soon as any switch input on any of the Raspberry devices changes state from Off (low) to On (high), all outputs (light) on all Raspberry devices toggle their state.


##Starting the Light Switch service

```python
Usage: $ sudo python light_switch_service.py {-n <name_prefix} { -i <pin_number> } { -o <pin_number> } <channel_name> <channel_password>  

       channel_name ::= string
               fully qualified channel name

       channel_password ::= string
               channel access password set by the channel owner

       pin_number ::= int 
               Number of the pin on Raspberry Pi port P1 which will be used
               as input (-i) or output (-o). More than one pin can be specified 
               of each type, but at least one pin number must be given (input or output) 
       
       name_prefix ::= string 
               Raspberry device name prefix
               If not set, defaults to 'RasPi'
```



**Examples:**

The following command will start the service using pin #15 as the output to which the light is connected and pin #16 as input where switch is connected. 
The communication will go through the channel whose fully qualified name is johnsmith.myhome where the access password set by the owner is jspwd

`$sudo python light_switch_service.py -o 15 -i 16 johnsmith.myhome jspwd`

The following command will connect to the same channel as above, but this time, both pin #15 and pin #16 will be configured as light outputs. 
They will independently listen to switch events coming through the channel and toggle their state in response.

`$sudo python light_switch_service.py -n MyPi -o 15 -o 16 johnsmith.myhome jspwd`

Note the use of -n option to assign a unique name to your Raspberry Pi device. If the -n option is not set the prexif is assumed to be 'RasPi' and if you have two or more devices running this script, the use of -n option ensures that the device names in the same channel do not clash.


NOTE: On Raspberry Pi the scripts must be run with root privileges (sudo) to be able to access GPIO.




