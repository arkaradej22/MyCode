import json
import requests
import subprocess
import sys
import base64
import xml.dom.minidom
from ncclient import manager
from tabulate import tabulate
from MheeMheeSharingFunction import *
import xmldict

def Get_Config_State(ip_addr=""):
    print("Start function Get_Config_State of IP {0}".format(ip_addr))
    file = open("Netconf Credential.txt","r")
    Filter= "<filter><CISCO-CONFIG-MAN-MIB><ccmHistory></ccmHistory><ccmCTIDObjects></ccmCTIDObjects><ccmCLIHistoryCommandTable></ccmCLIHistoryCommandTable></CISCO-CONFIG-MAN-MIB></filter>"
    for line in file:
        Netconf_Device_Data=line.split()
        print(" Data from file :",Netconf_Device_Data)
        if(ip_addr==Netconf_Device_Data[0]):
            try:
                m=manager.connect(host=Netconf_Device_Data[0], port=Netconf_Device_Data[1], username=Netconf_Device_Data[2],password=Netconf_Device_Data[3], hostkey_verify=False,device_params={'name': 'default'},allow_agent=False, look_for_keys=False)
            except:
                print("****ERROR on Get_Config_State with False : Cannot connect to {0}".format(ip_addr))
                return False
            result=m.get(Filter)
            if(result!=False):
                print("Complete function Get_Config_State")
                m.close_session()
                return xmldict.xml_to_dict(result.xml)
            else:
                print("****ERROR on Get_Config_State with False : Cannot Get Netconf output from {0}".format(ip_addr))
                m.close_session()
                return False
           

def Get_Hostname(ip_addr=""):
    print("Start function Get_Hostname")
    file = open("Netconf Credential.txt","r")
    Filter="<filter><native xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\"><hostname></hostname></native></filter>"  # XML For filter hostname
    for line in file:
        Netconf_Device_Data=line.split()
        print(" Data from file :",Netconf_Device_Data)
        if(ip_addr==Netconf_Device_Data[0]):
            try:
                m=manager.connect(host=Netconf_Device_Data[0], port=Netconf_Device_Data[1], username=Netconf_Device_Data[2],password=Netconf_Device_Data[3], hostkey_verify=False,device_params={'name': 'default'},allow_agent=False, look_for_keys=False)
            except:
                print("Finsih function Get_Device_InterfaceState_XML with False : Cannot connect to {0}".format(ip_addr))
                return "Unknown"
            result=m.get(Filter)
            if(result!=False):
                xml_doc = xml.dom.minidom.parseString(result.xml)
                Hostname = xml_doc.getElementsByTagName("hostname")
            m.close_session()
            print("Complete function Get_Hostname")
            return Hostname[0].firstChild.nodeValue

def Get_Device_Status_Netconf_List(file="",ip_addr=""):
    print("Start Function Get_Device_Status_Netconf_List")
    j=0
    device_list=[]
    for line in file:
        Netconf_Device_Data=line.split()
        print(" Data from file :",Netconf_Device_Data)
        PingResult=ping(Netconf_Device_Data[0])
        NetconfResult="Enable({0})".format(Netconf_Device_Data[1])
        try:
            m=manager.connect(host=Netconf_Device_Data[0], port=Netconf_Device_Data[1], username=Netconf_Device_Data[2],password=Netconf_Device_Data[3], hostkey_verify=False,device_params={'name': 'default'},allow_agent=False, look_for_keys=False)
            print("  Netconf Connect to {0} success".format(Netconf_Device_Data[0]))
            m.close_session()
        except:
            NetconfResult="Disable({0})".format(Netconf_Device_Data[1])
            print("  Netconf Connect to {0} fail".format(Netconf_Device_Data[0]))
            pass
        if(ip_addr.lower()=="all"):
            j+=1
            device_list.append([j,Netconf_Device_Data[0],PingResult,NetconfResult])
        elif(ip_addr==Netconf_Device_Data[0]):
            j+=1
            device_list.append([j,Netconf_Device_Data[0],PingResult,NetconfResult])

    print("Complete Function Get_Device_Status_Netconf_List")
    if(j==0):
        return "Device not found"
    else:
        return device_list #[0]=No.[1]=IP , [2]= Ping ,[3]=Netconf

def Get_Device_Status_Netconf(ip_addr=""):
    print("Start Function Get_Device_Status_Netconf")
    OutputMessage="Fail to get Netconf Device Status : "
    file = open("Netconf Credential.txt","r")
    device_list=Get_Device_Status_Netconf_List(file,ip_addr)
    if(device_list=="Device not found"):
        return OutputMessage+device_list
    else:
        OutputMessage=tabulate(device_list,headers=[' No.','| IP ','| Ping Status ','| Netconf Enable '],tablefmt="simple")
    print(OutputMessage)
    print("Finish Function Get_Device_Status_Netconf")   
    return OutputMessage
    
def Get_Device_InterfaceState_XML(ip_addr='',interface_filter='all'):

    print("start function Get_Device_InterfaceState_XML ")
    OutputMessage="Fail to get Netconf interface-state : "
    file = open("Netconf Credential.txt","r")
    Filterstart="<filter><interfaces-state><interface><type xmlns:ianaift=\"urn:ietf:params:xml:ns:yang:iana-if-type\">ianaift:ethernetCsmacd</type>"
    if(interface_filter!='all'):
        FilterAdd="<name>"+interface_filter+"</name>"
        Filterstart+=FilterAdd
    Filterend="</interface></interfaces-state></filter>"
    Filter=Filterstart+Filterend

    #print("XML Filter :")
    #print(xml.dom.minidom.parseString(Filter).toprettyxml())
    
    for line in file:
        Netconf_Device_Data=line.split()
        print(" Data from file :",Netconf_Device_Data)
        if(ip_addr==Netconf_Device_Data[0]):
            try:
                m=manager.connect(host=Netconf_Device_Data[0], port=Netconf_Device_Data[1], username=Netconf_Device_Data[2],password=Netconf_Device_Data[3], hostkey_verify=False,device_params={'name': 'default'},allow_agent=False, look_for_keys=False)
            except:
                print("Finsih function Get_Device_InterfaceState_XML with False : Cannot connect to {0}".format(ip_addr))
                return False
            output=m.get(Filter)
            print("Finsih function Get_Device_InterfaceState_XML with Output")
            m.close_session()
            return output

def Get_Device_InterfaceState(SubCommand):
    print("start function Get_Device_InterfaceState ")
    if(len(SubCommand)>3):
        result=Get_Device_InterfaceState_XML(SubCommand[1],SubCommand[3])
    else:
        result=Get_Device_InterfaceState_XML(SubCommand[1])
    #print(xml.dom.minidom.parseString(result.xml).toprettyxml())
    xml_doc = xml.dom.minidom.parseString(result.xml)
    name = xml_doc.getElementsByTagName("name")
    admin_status = xml_doc.getElementsByTagName("admin-status")
    oper_status = xml_doc.getElementsByTagName("oper-status")
    in_unicast = xml_doc.getElementsByTagName("in-unicast-pkts")
    in_multicast =xml_doc.getElementsByTagName("in-multicast-pkts")
    in_broadcast = xml_doc.getElementsByTagName("in-broadcast-pkts")
    out_unicast = xml_doc.getElementsByTagName("out-unicast-pkts")
    out_multicast =xml_doc.getElementsByTagName("out-multicast-pkts")
    out_broadcast = xml_doc.getElementsByTagName("out-broadcast-pkts")
    in_discard = xml_doc.getElementsByTagName("in-discards")
    in_error = xml_doc.getElementsByTagName("in-errors")
    out_discard = xml_doc.getElementsByTagName("out-discards")
    out_error = xml_doc.getElementsByTagName("out-errors")
    print (len(name),len(admin_status),len(oper_status),len(in_unicast),len(in_broadcast),len(in_multicast),len(out_unicast),len(out_multicast),len(out_broadcast),len(out_error),len(out_discard),len(in_discard),len(in_error))
    if(len(name)!=0):
        OutputMessage=""
        for i in range(0,len(name)):
            PacketInAll= int(in_unicast[i].firstChild.nodeValue)+int(in_multicast[i].firstChild.nodeValue)+int(in_broadcast[i].firstChild.nodeValue)
            PacketOutAll= int(out_unicast[i].firstChild.nodeValue)+int(out_multicast[i].firstChild.nodeValue)+int(out_broadcast[i].firstChild.nodeValue)
            OutputMessage+="\n----------"
            OutputMessage+="\nInterface name : "+name[i].firstChild.nodeValue
            OutputMessage+="\n  Admin Status : "+admin_status[i].firstChild.nodeValue
            OutputMessage+="\n  Operation Status : "+oper_status[i].firstChild.nodeValue
            OutputMessage+="\n  Pkt in : "+ str(PacketInAll)
            OutputMessage+="\n  Pkt out : "+ str(PacketOutAll)
            OutputMessage+="\n  input error : "+ in_error[i].firstChild.nodeValue
            OutputMessage+="\n  input drop : "+ in_discard[i].firstChild.nodeValue
            OutputMessage+="\n  output error : "+ out_error[i].firstChild.nodeValue
            OutputMessage+="\n  output discard :"+ out_discard[i].firstChild.nodeValue
        return OutputMessage+"\n----------"
    else:
        return "Not have interface name {0}".format(SubCommand[3])