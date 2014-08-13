# fi24_raspi_demo1

This projects serves as a demonstration of how followit24.com channels can be used to easily implement a distributed *hallway switch* functionality using a few Rasberry Pi's  
The functionality of this demonstration system is rather simple:  

- one Raspberry runs python script implementing the Light Service  
- other Rasberry devices run python script implementing the Switch Service
- as soon as any Switch Service changes state from Off to On (i.e. sends SwitchOn event) the state of the light toggles






