'''
@author: Piotr Orzechowski
@summary: This module contains definitions of URI's for services implemented and used by the
devices
'''

'''Discovery service'''
URI_DISCOVERY             = "com.followit24.service.discovery"
URI_DISCOVERY_GETSERVICES = "com.followit24.service.discovery.GetServices"
URI_DISCOVERY_SERVICELIST = "com.followit24.service.discovery.ServiceList"


'''Switch service'''
URI_SWITCH                = "com.followit24.service.switch"
URI_SWITCH_GETSTATE       = "com.followit24.service.switch.GetState"
URI_SWITCH_CURSTATE       = "com.followit24.service.switch.CurrentState"
URI_SWITCH_EV_SWITCHON       = "com.followit24.service.switch.SwitchedOn"
URI_SWITCH_EV_SWITCHOFF       = "com.followit24.service.switch.SwitchedOff"

'''Light service'''
URI_LIGHT                 ="com.followit24.service.light"
URI_LIGHT_CMD_ON          ="com.followit24.service.light.On"
URI_LIGHT_CMD_OFF          ="com.followit24.service.light.Off"
URI_LIGHT_CMD_TOGGLE       ="com.followit24.service.light.Toggle"
URI_LIGHT_CMD_GETSTATE       ="com.followit24.service.light.GetState"
URI_LIGHT_RSP_CURSTATE       ="com.followit24.service.light.CurrentState"

