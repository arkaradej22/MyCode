#!/usr/bin/env python
#
# Get configured interfaces using Netconf
#
# darien@sdnessentials.com
#

from ncclient import manager
import sys
import xml.dom.minidom
import xmldict
import json

# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device

HOST = '10.20.98.1'
# use the NETCONF port for your IOS-XE device
PORT = 830
# use the user credentials for your IOS-XE device
USER = 'msc'
PASS = 'Cisco@2016'
# XML file to open
FILE = 'Test_Netconf_Script.xml'
"""
# use the IP address or hostname of your CSR1000V device
HOST = 'ios-xe-mgmt.cisco.com'
# use the NETCONF port for your IOS-XE device
PORT = 10000
# use the user credentials for your IOS-XE device
USER = 'root'
PASS = 'D_Vay!_10&'
FILE = 'Test_Netconf_Script.xml'
# create a main() method
"""
def get_Netconf_result(xml_filter):
    """
    Main method that retrieves the interfaces from config via NETCONF.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,password=PASS, hostkey_verify=False,device_params={'name': 'default'},allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
                #return(m.edit_config(target="running",config=f.read(), format='xml'))
            #print (m.server_capabilities)
            return(m.get(f.read()))
                #return(m.get_config("running",f.read(),))
                #return(m.dispatch(f.read()))


def main():
    """
    Simple main method calling our function.
    """
    interfaces = get_Netconf_result(FILE)
    temp=xml.dom.minidom.parseString(interfaces.xml).toprettyxml()
    file = open("Netconf_result.xml","w")
    file.write(temp)
    
    
    dict1=xmldict.xml_to_dict(interfaces.xml)
    file = open("Netconf_result.json","w")
    file.write(json.dumps(dict1,indent=4))
    #print(xml.dom.minidom.parseString(interfaces.xml).toprettyxml())

if __name__ == '__main__':
    sys.exit(main())
