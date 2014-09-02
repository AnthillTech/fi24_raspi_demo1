'''
@author: Piotr Orzechowski
@summary: This module contains definitions of URI's for services implemented and used by the
devices
'''

'''Discovery service'''
URI_DISCOVERY             = "org.fi24.discovery"
URI_DISCOVERY_GETSERVICES = "org.fi24.discovery.GetServices"
URI_DISCOVERY_SERVICELIST = "org.fi24.discovery.ServiceList"


'''Switch service'''
URI_SWITCH                = "org.fi24.switch"
URI_SWITCH_GETSTATE       = "org.fi24.switch.GetState"
URI_SWITCH_CURSTATE       = "org.fi24.switch.CurrentState"
URI_SWITCH_EV_SWITCHON       = "org.fi24.switch.SwitchedOn"
URI_SWITCH_EV_SWITCHOFF       = "org.fi24.switch.SwitchedOff"

'''Light service'''
URI_LIGHT                 ="org.fi24.light"
URI_LIGHT_CMD_ON          ="org.fi24.light.TurnOn"
URI_LIGHT_CMD_OFF          ="org.fi24.light.TurnOff"
URI_LIGHT_CMD_TOGGLE       ="org.fi24.light.Toggle"
URI_LIGHT_EVT_TURNEDON       ="org.fi24.light.TurnedOn"
URI_LIGHT_EVT_TURNEDOFF       ="org.fi24.light.TurnedOff"

