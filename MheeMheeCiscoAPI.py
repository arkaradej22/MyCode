from MheeMheeSharingFunction import *
from MheeMheeCiscoNetConf import *
from ncclient import manager
from tabulate import tabulate
import json
import requests
import subprocess
import sys
import base64
def Get_CommandResult(Command=""):
    print ("Start Function Get_CommandResult")
    print ("Input Command : \"{0}\"".format(Command))
    OutputMessage="This function was enable in Future"
    ## Split Text To List
    SubCommand=Command
    print ("Split Command=",SubCommand)
    print ("Amount of Command=",len(SubCommand))
    if(SubCommand[1].lower()=='device'):
        if(SubCommand[2].lower()=='status'):
            if(SubCommand[3].lower()=='all' and len(SubCommand)==4):
                OutputMessage=Get_Device_Status(SubCommand[3].lower())
            elif(validate_ip(SubCommand[3])and len(SubCommand)==4):
                OutputMessage=Get_Device_Status(SubCommand[3])
            elif(SubCommand[3].lower()=='all' and len(SubCommand)>=4):
                OutputMessage=Get_Device_Status_Netconf(SubCommand[3])
            elif(validate_ip(SubCommand[3]) and len(SubCommand)>=4):
                OutputMessage=Get_Device_Status_Netconf(SubCommand[3])
            else:
                OutputMessage="Error After \'Get Device Status \' : IP Format Wrong" 
        else:
            OutputMessage="Error After \'Get Device\' : Not have command {0} in Command List".format(SubCommand[2])
    elif(validate_ip(SubCommand[1])):
        if(SubCommand[2]=='interface'):
            OutputMessage=Get_Device_InterfaceState(SubCommand)
        else:
            OutputMessage="Error After \'Get "+SubCommand[1]+" Status \' : command not existing"
    else:
        OutputMessage="Error After \'Get Device\' : Not have command {0} in Command List".format(SubCommand[1])
    print ("Finish Function Get_CommandResult")
    return OutputMessage

def Get_Device_Status(ip_addr=""):
    print("Start Function Get_Device_Status")
    file = open("API Credential.txt","r")
    OutputMessage="Fail to get Device Status : "
    for line in file:
        Appliance_Data=line.split()
        print(" Data from file :",Appliance_Data)
        if(Appliance_Data[0]=="CiscoPrime"):
            URL='https://'+Appliance_Data[1]+'/webacs/api/v1/data/Devices.json?.full=true'
            userandpass=Appliance_Data[2]+":"+Appliance_Data[3]
            a=base64.b64encode(bytes(userandpass, 'utf-8'))
            headers = {
                "authorization":"Basic "+str(a)[2:26],
                #"Authorization": "Basic cm9vdDpOZXR3MHJrQE1TQw=="
            }
            print(" Url =",URL)
            print(" header =",json.dumps(headers,indent=4))
            respond = requests.request("GET", URL, headers=headers,verify=False)
            result = respond.json()
            device_list=[]
            j=0
            for i in result["queryResponse"]["entity"]:
                print(ip_addr,type(ip_addr),i["devicesDTO"]["ipAddress"],type(i["devicesDTO"]["ipAddress"]),ip_addr==i["devicesDTO"]["ipAddress"])
                if(ip_addr.lower()=="all"):
                    j+=1
                    device_list.append([j,i["devicesDTO"]["deviceName"],i["devicesDTO"]["ipAddress"],i["devicesDTO"]["reachability"]])
                elif(ip_addr==i["devicesDTO"]["ipAddress"]):
                    #print("Yeah Yeah Finally I Found Matching from {0} and {1}".format(ip_addr,i["devicesDTO"]["ipAddress"]))
                    j+=1
                    device_list.append([j,i["devicesDTO"]["deviceName"],i["devicesDTO"]["ipAddress"],i["devicesDTO"]["reachability"]])
                

            if(j==0):
                return OutputMessage+"Device not found"
            OutputMessage=tabulate(device_list,headers=['No.','hostname','ip','status'],tablefmt="simple")
    print(OutputMessage)
    print("Finish Function Get_Device_Status")   
    return OutputMessage

