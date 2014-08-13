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
URI_SWITCH_CURSTATE       = "com.followit24.service.switch.CurState"
URI_SWITCH_EV_SWITCHON       = "com.followit24.service.switch.SwitchOn"
URI_SWITCH_EV_SWITCHOFF       = "com.followit24.service.switch.SwitchOff"