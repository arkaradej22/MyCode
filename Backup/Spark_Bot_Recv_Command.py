from flask import Flask, request
from MheeMheeSparkBot import *
from tabulate import tabulate
import sys
import base64
Bot_Authorization = 'Bearer Y2M5YTY3NDktZDU4YS00ZTIyLWJiZjMtZWUzODM2NjJkODIwMjE0M2JhYWMtOTJj'
User_Authorization = "Bearer M2ExNDJkMzItYjQxMi00ZWQzLTgxMTktMjU5YzI0ZDllOWU3MWVjNWVhNjAtZmU0"


app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def index():
    json_line = request.get_json()
    #decoded['data']['id']
   #print(json.dumps(json_line,indent=4))
    MessageText=Get_Spark_message(json_line["data"]["id"],User_Authorization)
    print(" Bot Recv Message form Spark : ",MessageText)

    if("mentionedPeople" in json_line["data"]):
        #print ("Have mention to MheeMheeBot  | token =",json_line["data"]["mentionedPeople"])
        #json_line["data"]["mentionedPeople"]==Bot_ID
        for i in json_line["data"]["mentionedPeople"]:
            if(i=='Y2lzY29zcGFyazovL3VzL1BFT1BMRS9kMDY2YzZjNC04MTZmLTQ5YzMtOWQwYi1kYTMxM2NjMGQ3MDM'):
                Command=MessageText[12:].split() # Cut @MheeMheeBot out.
                PersonName=Get_Spark_PersonName(json_line["data"]["personId"],Bot_Authorization)
                print("Command = ",Command)
                if(Command[0].lower()=="hello"): #Check command Hello for test Bot Connection
                   SendMessage="Hello {0}".format(PersonName)
                   print("Send Message following to sparkroom : \" {0} \"".format(SendMessage))
                   SendResult=Post_Message_To_Sparkroom(json_line["data"]["roomId"],SendMessage,Bot_Authorization)
                   print(SendResult)
                elif(Command[0].lower()=="help"):#Check command Help and send command list
                    SendMessage=Get_Help_Message(PersonName)
                    print("Send Message following to sparkroom : \" {0} \"".format(SendMessage))
                    SendResult=Post_Message_To_Sparkroom(json_line["data"]["roomId"],SendMessage,Bot_Authorization)
                elif(Command[0].lower()=="get"):#Check command Get and send Result
                    print("send get result to user name : ",PersonName)
                    SendMessage=Get_CommandResult(Command)
                    print("Send Message following to sparkroom :\n \" {0} \"".format(SendMessage))
                    SendResult=Post_Message_To_Sparkroom(json_line["data"]["roomId"],SendMessage,Bot_Authorization)
                    print(SendResult)
                else:
                    print("MheeMhee Not Understand command : Not have suffix get,help,hello")
            else:
                print("MheeMhee Not interest command : Not have one mention me")
    else:
        print("MheeMhee Not interest : Not mention to anyone")
    return "200"


if __name__ == '__main__':
     app.run(debug=True,port=8080)