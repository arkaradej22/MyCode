from ncclient import manager
from tabulate import tabulate
from MheeMheeSharingFunction import *
from MheeMheeCiscoAPI import *
import json
import requests
import subprocess
import sys
import base64

Bot_Authorization = 'Bearer X0Ahhzcq9XyxPHHFazjKD3LqZHIEWioXqwI2qIATDAOj9L6RNGxaa+e8mPdwYkPGpejwfYsnG5/kRRq5jhtkACnJM24ZBanbcbq7VS2rhscD1rH/w7L0iae27oPbW53RSVg2Bq1rKzjgb/DAFZW1mgdB04t89/1O/w1cDnyilFU='
User_Authorization = "Bearer M2ExNDJkMzItYjQxMi00ZWQzLTgxMTktMjU5YzI0ZDllOWU3MWVjNWVhNjAtZmU0"

def Get_Help_Message(PersonName=""):
    Message="Hi "+PersonName+"\n"
    Message+="This is all command we support now\n"
    Message+="   Get Device status [IP_Addr|ALL]\n"
    Message+="   Get Device status [IP_Device|All] netconf \n"
    Message+="   Get [IP_Device] Interface { Interface_Name }\n"
    Message+="   Add Device [APIC-EM|Prime|Netconf] [IP] [Port] [Username] [Password]\n"
    Message+="   List Device [APIC-EM|Prime|Netconf]\n"
    return Message

def Get_Line_PersonName(PersonID="",Authorization=""):
	print ("Start Get_Line_PersonName")
	#https://api.line.me/v2/bot/profile/User_ID
	URL='https://api.line.me/v2/bot/profile/{0}'.format(PersonID)
	print("Url =",URL)
	headers = {
        'content-type': "application/json",
        'authorization': Authorization,
        }
	respond = requests.request("GET", URL, headers=headers)
	result = respond.json()
	print(" return Value : {0} ".format(result['displayName']))
	print("end Function Get_Spark_Message\n")
	print ("End Get_Line_PersonName")
	return result['displayName']


def Post_Message_To_LineGroup(RoomID="",SendMessage="",Authorization=""):
    print("Start Function Post_Message_To_Sparkroom")
    URL='https://api.line.me/v2/bot/message/push'
    MessageBlock=SendMessage.split('\n')
    print("Message Block = {0}".format(len(MessageBlock)))
    WordCount=0 # count text not more than 1600
    SendBlock=""#String that send in eack block
    headers = {
        "content-type": "application/json",
        "authorization": Authorization,
    }

    ## Line have limitation with 2000 charecter per 1 text message if we detect lengh of sendmessage more than 1600 we will send it first
    for i in range(0,len(MessageBlock)):
    	## Check Lenght of SendBlock -> If WordCount more than 1600 or i is last messageblock-> send to user and clear value
    	SendBlock+=MessageBlock[i] #add message to send block
    	SendBlock+="\n" ##add new line
    	WordCount+=len(MessageBlock[i])
    	print("i={0},MessageBlock={1},WordCount=,{2}".format(i,MessageBlock[i],WordCount))
    	if(MessageBlock[i]=='----------' or i==len(MessageBlock)-1):
    		if(WordCount+len(MessageBlock[i])>=1600 or i==len(MessageBlock)-1):
    			payload = {
				"to": RoomID,
        		"messages": [
        				{ 
        					"type": "text",
        					"text": SendBlock
        				}
        			]
    			}
    			print(" Url =",URL)
    			print(" header =",json.dumps(headers,indent=4))
    			print(" body = ",json.dumps(payload,indent=4))
    			print("lenght of string = {0}".format(WordCount))
    			respond = requests.request("POST",URL, headers=headers,data=json.dumps(payload,indent=4))
    			if(respond.status_code!=200):
    				return respond.status_code,respond.reason,respond.text
    		#Clear Value after send
    			WordCount=len(MessageBlock[i])
    			SendBlock=""
    	
    print("End Function Post_Message_To_Sparkroom")
    return respond.status_code,respond.reason,respond.text
