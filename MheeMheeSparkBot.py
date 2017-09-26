from MheeMheeSharingFunction import *
from MheeMheeCiscoAPI import *
import json
import requests
import subprocess
import sys
import base64

def Get_Help_Message(PersonName=""):
    Message="Hi "+PersonName+" \n"
    Message+="This is all command we support now \n"
    Message+="   Get Device status [IP_Addr|ALL] \n"
    Message+="   Get Device status [IP_Device|All] netconf \n"
    Message+="   Get [IP_Device] Interface { Interface_Name } \n"
    Message+="   Add Device [APIC-EM|Prime|Netconf] [IP] [Port] [Username] [Password] \n"
    Message+="   List Device [APIC-EM|Prime|Netconf] \n"
    #Message+="   Get Host [host-ip|ALL] [APIC-EM|Prime|all]\n"
    #Message+="   Trace From [host1_ip] to [host2_ip]\n"
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


