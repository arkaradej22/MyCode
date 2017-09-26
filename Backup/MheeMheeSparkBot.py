from ncclient import manager
from tabulate import tabulate
import json
import requests
import subprocess
import sys
import base64

def Get_Help_Message(PersonName=""):
    Message="Hi "+PersonName+"\n"
    Message+="This is all command we support now\n"
    Message+="   Get Device status {IP_Addr|ALL}\n"
    Message+="   Get Device status {IP_Device|All} netconf \n"
    Message+="   Get Interface status [IP_Device] {Interface_Name|ALL}\n"
    Message+="   Get Interface state [IP_Device] {Interface_Name|ALL}\n"
    return Message


def Post_Message_To_Sparkroom(RoomID="",SendMessage="",Authorization=""):
    print("Start Function Post_Message_To_Sparkroom")
    URL='https://api.ciscospark.com/v1/messages'
    
    headers = {
        "content-type": "application/json",
        "authorization": Authorization,
    }
    payload = {
        "roomId": RoomID,
        "text": SendMessage,
    }
    print(" Url =",URL)
    print(" header =",json.dumps(headers,indent=4))
    print(" body = ",json.dumps(payload,indent=4))
    respond = requests.request("POST",URL, headers=headers,data=json.dumps(payload,indent=4))
    return respond.status_code,respond.reason

def Get_Spark_PersonName(PersonID="",Authorization=""):
    print("Start Function Get_PersonName")
    URL='https://api.ciscospark.com/v1/people/{0}'.format(PersonID)
    print(" Url =",URL)
    #print("\n headers =",headers)
    headers = {
        'content-type': "application/json",
        'authorization': Authorization,
        }
    respond = requests.request("GET", URL, headers=headers)
    result = respond.json()
    print(" return Value : {0} ".format(result["displayName"]))
    print("end Function Get_PersonName\n")
    return result["displayName"]

def Get_Spark_PersonNameInRoom(RoomID="",PersonID="",Authorization=""):
    print("Start Function Get_Spark_Room")
    URL='https://api.ciscospark.com/v1/memberships?roomId={0}/&personId={1}'.format(RoomID,PersonID)
    print("Url =",URL)
    #print("\n headers =",headers)
    headers = {
        'content-type': "application/json",
        'authorization': Authorization,
        }
    respond = requests.request("GET", URL, headers=headers)
    result = respond.json()
    print(" return Value : {0} ".format(result["items"][0]["personDisplayName"]))
    print("end Function Get_Spark_Message\n")
    return result["items"][0]["personDisplayName"]

def Get_Spark_message(MessageID="",Authorization=""):
    print("Start Function Get_Spark_Message")
    URL='https://api.ciscospark.com/v1/messages/{0}'.format(MessageID)
    headers = {
        'content-type': "application/json",
        'authorization': Authorization,
        }
    print("Url =",URL)
    #print("\n headers =",headers)
    respond = requests.request("GET", URL, headers=headers)
    result = respond.json()
    #print(json.dumps(result,indent=4))
    print(" return Value : {0} ".format(result["text"]))
    print("end Function Get_Spark_Message\n")
    return result["text"]

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
    print ("Finish Function Get_CommandResult")
    return OutputMessage

def Get_Device_Status_Netconf(ip_addr=""):
    print("Start Function Get_Device_Status_Netconf")
    OutputMessage="Fail to get Netconf Device Status : "
    file = open("Netconf Credential.txt","r")
    j=0
    device_list=[]
    for line in file:
        Netconf_Device_Data=line.split()
        print(" Data from file :",Netconf_Device_Data)
        PingResult=ping(Netconf_Device_Data[0])
        NetconfResult="Enable({0})".format(Netconf_Device_Data[1])
        try:
            m=manager.connect(host=Netconf_Device_Data[0], port=Netconf_Device_Data[1], username=Netconf_Device_Data[2],password=Netconf_Device_Data[3], hostkey_verify=False,device_params={'name': 'default'},allow_agent=False, look_for_keys=False)

        except:
            NetconfResult="Disable({0})".format(Netconf_Device_Data[1])
            pass
        if(ip_addr.lower()=="all"):
            j+=1
            device_list.append([j,Netconf_Device_Data[0],PingResult,NetconfResult])
        elif(ip_addr==Netconf_Device_Data[0]):
            j+=1
            device_list.append([j,Netconf_Device_Data[0],PingResult,NetconfResult])

    if(j==0):
        return OutputMessage+"Device not found"
    OutputMessage=tabulate(device_list,headers=[' No.','| IP ','| Ping Status ','| Netconf Enable '],tablefmt="simple")
    print(OutputMessage)
    print("Finish Function Get_Device_Status_Netconf")   
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

def validate_ip(ip_addr=""):
    a = ip_addr.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def ping(hostname):
    p = subprocess.Popen('ping ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pingStatus = 'ok';
        
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
 
        if (output.endswith('unreachable.')) :
            #No route from the local system. Packets sent were never put on the wire.
            pingStatus = 'unreacheable'
            break
        elif (output.startswith('Ping request could not find host')) :
            pingStatus = 'host_not_found'
            break
        if (output.startswith('Request timed out.')) :
            #No Echo Reply messages were received within the default time of 1 second.
            pingStatus = 'timed_out'
            break
        #end if
    #endFor
    return pingStatus
#endDef    