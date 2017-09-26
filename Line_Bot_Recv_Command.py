from flask import Flask, request
import json
from MheeMheeLineBot import *
from MheeMheeCiscoAPI import *

app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def index():
	json_line = request.get_json()
    #decoded['data']['id']
	print(json.dumps(json_line,indent=4))
	if(json_line['events'][0]['message']['text'][0:2]=="X1" or json_line['events'][0]['message']['text'][0:2]=="x1"):
		Command=json_line['events'][0]['message']['text'][3:].split()
		if(len(Command)==0):
			print("Hi My name is X1 \n I'm now the mobility notification and get some command for you \n use \"X1 Help \" Command to check all my support command")
			print(Post_Message_To_LineGroup(json_line['events'][0]['source']['groupId'],"Hi My name is X1 \n I'm now the mobility notification and get some command for you \n use \"X1 Help \" Command to check all my support command",Bot_Authorization))
			return "200"
		else:

			print ("Command from line = ",Command)
			PersonName=Get_Line_PersonName(json_line['events'][0]['source']['userId'],Bot_Authorization)
			if(Command[0].lower()=="hello"): #Check command Hello for test Bot Connection
				SendMessage="Hello {0}".format(PersonName)
				print("Send Message following to sparkroom : \" {0} \"".format(SendMessage))
				print(Post_Message_To_LineGroup(json_line['events'][0]['source']['groupId'],SendMessage,Bot_Authorization))
			elif(Command[0].lower()=="help"):#Check command Help and send command list
				SendMessage=Get_Help_Message(PersonName)
				print("Send Message following to sparkroom : \" {0} \"".format(SendMessage))
				SendResult=Post_Message_To_LineGroup(json_line['events'][0]['source']['groupId'],SendMessage,Bot_Authorization)
			elif(Command[0].lower()=="get"):#Check command Get and send Result
				print("send get result to user name : ",PersonName)
				SendMessage=Get_CommandResult(Command)
				print("Send Message following to sparkroom :\n \" {0} \"".format(SendMessage))
				SendResult=Post_Message_To_LineGroup(json_line['events'][0]['source']['groupId'],SendMessage,Bot_Authorization)
				print(SendResult)	
			elif(Command[0].lower()=="add"):
				print("Add Device To Data Store")
				AddResult=Add_Device(Command)
				SendMessage="Result of AddDevice : "+AddResult
				SendMessage="Hi "+PersonName+"\n"+SendMessage
				SendMessage=List_Device(Command)
				print(SendMessage)
				SendResult=Post_Message_To_LineGroup(json_line['events'][0]['source']['groupId'],SendMessage,Bot_Authorization)
			elif(Command[0].lower()=="list"):
				print("list Device in Data Store")
				#SendMessage="Hi "+PersonName+"\n"+SendMessage
				print(SendMessage)
				SendResult=Post_Message_To_LineGroup(json_line['events'][0]['source']['groupId'],SendMessage,Bot_Authorization)
			else:
				print("X1 Not Understand command : Not have suffix get,help,hello,add,list")

	return "200"	
			

if __name__ == '__main__':
     app.run(debug=True,port=8080)

