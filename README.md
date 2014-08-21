# fi24_raspi_demo1

This projects serves as a demonstration of how followit24.com channels can be used to easily implement a distributed *hallway switch* functionality using one or more Raspberry Pi
The functionality of this demonstration system is rather simple:  

- you start the Light Switch service on each Raspberry Pi that you want to work in the network. 
- command line options determine which GPIO pins are outputs (light) or inputs (switch)
- as soon as any switch input on any of the Raspberry devices changes state from Off (low) to On (high), all outputs (light) on all Raspberry devices toggle their state.


##Starting the Light Switch service

```python
Usage: $ sudo python light_switch_service.py { -i <pin_number> } { -o <pin_number> } <channel_name> <channel_password>  

       channel_name ::= string
               fully qualified channel name

       channel_password ::= string
               channel access password set by the channel owner

       pin_number ::= int 
               Number of the pin on Raspberry Pi port P1 which will be used
               as input (-i) or output (-o). More than one pin can be specified 
               of each type, but at least one pin number must be given (input or output) 
```

NOTE: the script must be run with root privileges (sudo) to be able to access GPIO




