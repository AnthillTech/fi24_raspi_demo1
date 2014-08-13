# fi24_raspi_demo1

This projects serves as a demonstration of how followit24.com channels can be used to easily implement a distributed *hallway switch* functionality using a few Rasberry Pi's  
The functionality of this demonstration system is rather simple:  

- one Raspberry runs python script implementing the Light Service  
- other Rasberry devices run python script implementing the Switch Service
- as soon as any Switch Service changes state from Off to On (i.e. sends SwitchOn event) the state of the light toggles

##Starting the Switch service

```python
Usage: python switch_service.py -c <channel_name> -p <channel_password> -i <pin_number>  { -i <pin_number> }   

       channel_name ::= string
               fully qualified channel name

       channel_password ::= string
               channel access password set by the channel owner

       pin_number ::= int 
               Number of the pin on Raspberry Pi port P1 which will be used
               as input. More than one pin can be specified

```


##Starting the Light service

```python
Usage: python light_service.py -c <channel_name> -p <channel_password> -o <pin_number>  { -o <pin_number> }   

       channel_name ::= string
               fully qualified channel name

       channel_password ::= string
               channel access password set by the channel owner

       pin_number ::= int 
               Number of the pin on Raspberry Pi port P1 which will be used
               as output. More than one pin can be specified

```




