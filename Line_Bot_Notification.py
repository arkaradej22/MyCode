import json
import time
from MheeMheeLineBot import *
from MheeMheeCiscoAPI import *

def Detect_Device_Status():
	device_list=[]
	print("Start Function Device_Status")
	OutputMessage="Fail to get Netconf Device Status : "
	file = open("Netconf Credential.txt","r")
	device_list=Get_Device_Status_Netconf_List(file,"all")
	#print("   Return Device List :{0}".format(device_list))
	print("complete Function Device_Status") #[0]=No.[1]=IP , [2]= Ping ,[3]=Netconf
	if(device_list!="Device not found"):
		return device_list 
	else:
		return []	

def Detect_Monitor_State(Current=[]):
	Return_list=[]
	Dict_OneDeviceStatus={} 
	ListTemp_All_Interface=[]
	DictTemp_Interface_State={}
	"""
	[
		{
  			IP : ""
  			Hostname : ""
  			PingStatus : ""
  			NetconfStatus : ""
  			RunningLastChanged:""
  			StartupLastChanged:""
  			WhoChanged:""
  			LastChangeDate:""
  			LastChangeTime:""
  			CommandList:[COMMAND1,COMMAND2...]
  			Interface-state:[
  				{
  					name :
  					Oper_Status:
  					inerr :
  					indiscard :
  					outerr :
  					outdis :
  				},
  			]
  			
			
		},
	]
	"""
	print("Start Function Detect_Monitor_State")
	for DataDeviceStatus in Current:
		Dict_OneDeviceStatus['IP']=DataDeviceStatus[1]
		Dict_OneDeviceStatus['Hostname']=Get_Hostname(DataDeviceStatus[1])
		Dict_OneDeviceStatus['PingStatus']=DataDeviceStatus[2]
		Dict_OneDeviceStatus['NetconfStatus']=DataDeviceStatus[3]
		if(DataDeviceStatus[3][:6].lower()=='enable'): # if IP address in list has ping status OK
			###Start Get IP , hostname , netconfstate ### 


			### Start Get Interface of Device ###
			result=Get_Device_InterfaceState_XML(DataDeviceStatus[1]) ## Input IP Output XML##
			if(result!=False):
				#print(xml.dom.minidom.parseString(result.xml).toprettyxml())
				xml_doc = xml.dom.minidom.parseString(result.xml)
				name = xml_doc.getElementsByTagName("name")
				oper_status = xml_doc.getElementsByTagName("oper-status")
				in_discard = xml_doc.getElementsByTagName("in-discards")
				in_error = xml_doc.getElementsByTagName("in-errors")
				out_discard = xml_doc.getElementsByTagName("out-discards")
				out_error = xml_doc.getElementsByTagName("out-errors")
				print (len(name),len(oper_status),len(out_error),len(out_discard),len(in_discard),len(in_error))
				for j in range(0,len(name)):
					DictTemp_Interface_State={}
					DictTemp_Interface_State['Name']=name[j].firstChild.nodeValue
					DictTemp_Interface_State['Oper_status']=oper_status[j].firstChild.nodeValue
					DictTemp_Interface_State['in_discard']=in_discard[j].firstChild.nodeValue
					DictTemp_Interface_State['in_error']=in_error[j].firstChild.nodeValue
					DictTemp_Interface_State['out_discard']=out_discard[j].firstChild.nodeValue
					DictTemp_Interface_State['out_error']=out_error[j].firstChild.nodeValue
					ListTemp_All_Interface.append(DictTemp_Interface_State)
				Dict_OneDeviceStatus['Interface_State']=ListTemp_All_Interface	
			else:
				print(" Fail To Get Interface Result : ****ERROR when use Function \"Get_Device_InterfaceState_XML\"\n")
			### Start Get Config-State of Device ###
			result2=Get_Config_State(DataDeviceStatus[1]) ## Input IP output Dict ##
			if(result2!=False):
				print(json.dumps(result2,indent=4))
				Dict_OneDeviceStatus['RunningLastChanged']=result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmHistory"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmHistoryRunningLastChanged"]
				Dict_OneDeviceStatus['StartupLastChanged']=result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmHistory"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmHistoryStartupLastChanged"]
				Dict_OneDeviceStatus['WhoChanged']=result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCTIDObjects"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCTIDWhoChanged"]
				Dict_OneDeviceStatus['LastChangeDate']=result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCTIDObjects"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCTIDLastChangeTime"].split(",")[0]
				Dict_OneDeviceStatus['LastChangeTime']=result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCTIDObjects"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCTIDLastChangeTime"].split(",")[1]
				print("\n RunningLastChanged={0}\n StartupLastChanged={1}\n WhoChanged={2}\n LastChangeDate={3}\n LastChangeTime={4}\n".format(Dict_OneDeviceStatus['RunningLastChanged'],Dict_OneDeviceStatus['StartupLastChanged'],Dict_OneDeviceStatus['WhoChanged'],Dict_OneDeviceStatus['LastChangeDate'],Dict_OneDeviceStatus['LastChangeTime']))

				if "{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCLIHistoryCommandTable" in result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]:
					Dict_OneDeviceStatus['CommandList']=[]
					for OneCommand in result2["{urn:ietf:params:xml:ns:netconf:base:1.0}rpc-reply"]["{urn:ietf:params:xml:ns:netconf:base:1.0}data"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}CISCO-CONFIG-MAN-MIB"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCLIHistoryCommandTable"]["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCLIHistoryCommandEntry"]:
						print("\nCommand : {0}".format(OneCommand["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCLIHistoryCommand"]))
						Dict_OneDeviceStatus['CommandList'].append(OneCommand["{urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB}ccmCLIHistoryCommand"])
			else:
				print(" Fail To Get Interface Result : ****ERROR when use Function \"Get_Config_State\"\n")

			Return_list.append(Dict_OneDeviceStatus)
			# Clear All Value after append
			Dict_OneDeviceStatus={}
			DictTemp_Interface_State={}
			ListTemp_All_Interface=[]
	print("complete Function Detect_Monitor_State") 
	return Return_list

def Compare_Monitor_Status(Current=[],LastTime=[]):
	Return_list=[]
	"""
	[
		{
			IP:""
			Hostname:""
			Config_Change:{
				Date:
				Time:
				User:
				CommandList:[]
			}
			Config_Save:Booleen
			ErrorInterface:[
				{
					Oper_Before:
					Oper_After:
					in_discard:
					in_error:
					out_discrd:
					out_error:
					name:
				}
			]
			
		}
	]
	"""
	DictTemp_OneDeviceStatus={}
	Listtemp_Error_interface=[]

	print("Start Function Compare_Monitor_Status")
	for CurrentOneDevice in Current:
		if(LastTime==[]):
			print("complete Function Detect Compare_Monitor_Status")
			return []
		else:
			for LastTimeOneDevice in LastTime:
				if(CurrentOneDevice['IP']==LastTimeOneDevice['IP'] and CurrentOneDevice['NetconfStatus'][:6]=='Enable'):
					DictTemp_OneDeviceStatus['IP']=CurrentOneDevice['IP']
					DictTemp_OneDeviceStatus['Hostname']=CurrentOneDevice['Hostname']
					DictTemp_OneDeviceStatus['Config_Change']={}
					DictTemp_OneDeviceStatus['Config_Save']=True
					# Detect Config Change
					if(CurrentOneDevice["RunningLastChanged"]>CurrentOneDevice["StartupLastChanged"]):
						DictTemp_OneDeviceStatus['Config_Save']=False
					if(CurrentOneDevice["LastChangeDate"]!=LastTimeOneDevice["LastChangeDate"] or CurrentOneDevice["LastChangeTime"]!=LastTimeOneDevice["LastChangeTime"]):
						DictTemp_OneDeviceStatus['Config_Change']['Date']=CurrentOneDevice['LastChangeDate']
						DictTemp_OneDeviceStatus['Config_Change']['Time']=CurrentOneDevice['LastChangeTime']
						DictTemp_OneDeviceStatus['Config_Change']['User']=CurrentOneDevice['WhoChanged']
						DictTemp_OneDeviceStatus['Config_Change']['CommandList']=CurrentOneDevice['CommandList']
					# 2 For loop for loop the interface state 
					for CurrentOneInterface in CurrentOneDevice['Interface_State']:
						for LastTimeOneInterface in LastTimeOneDevice['Interface_State']:
							### Compare Interface State
							if(CurrentOneInterface['Name']==LastTimeOneInterface['Name']):
								DictTemp_Interface={}
								Flag=False
								if(CurrentOneInterface['Oper_status']!=LastTimeOneInterface['Oper_status']):
									Flag=True
									DictTemp_Interface['Oper_Before']=LastTimeOneInterface['Oper_status']
									DictTemp_Interface['Oper_After']=CurrentOneInterface['Oper_status']
								if(CurrentOneInterface['in_discard']>LastTimeOneInterface['in_discard']):
									Flag=True
									DictTemp_Interface['in_discard']=int(CurrentOneInterface['in_discard'])-int(LastTimeOneInterface['in_discard'])
								if(CurrentOneInterface['in_error']>LastTimeOneInterface['in_error']):
									Flag=True
									DictTemp_Interface['in_error']=int(CurrentOneInterface['in_error'])-int(LastTimeOneInterface['in_error'])
								if(CurrentOneInterface['out_discard']>LastTimeOneInterface['out_discard']):
									Flag=True
									DictTemp_Interface['out_discard']=int(CurrentOneInterface['out_discard'])-int(LastTimeOneInterface['out_discard'])
								if(CurrentOneInterface['out_error']>LastTimeOneInterface['out_error']):
									Flag=True
									DictTemp_Interface['out_error']=int(CurrentOneInterface['out_error'])-int(LastTimeOneInterface['out_error'])
								if(Flag):
									DictTemp_Interface['Name']=CurrentOneInterface['Name']
									Listtemp_Error_interface.append(DictTemp_Interface)


					DictTemp_OneDeviceStatus['ErrorInterface']=Listtemp_Error_interface
			if(CurrentOneDevice['NetconfStatus'][:6]=='Enable'):
				Return_list.append(DictTemp_OneDeviceStatus)
			DictTemp_OneDeviceStatus={}
			Listtemp_Error_interface=[]
			DictTemp_Interface={}
	print("Finish Function Compare_Monitor_Status") 
	return Return_list

def Compare_Device_Status(Current="",LastTime=""):
	print ("Start Function Compare_Device_Status")
	Return_list=[] # [[IP1,LastTimeStatus,CurentStatus,Hostname],.....]
	for i in range(0,len(Current)):
		if (LastTime==[]):
			Return_list.append([Current[i][1],"Unknown",Current[i][2]])
		else:
			for j in range(0,len(LastTime)):
				if(Current[i][1]==LastTime[j][1] and (Current[i][2]!=LastTime[i][2] and Current[i][3]!=Current[i][3])):
					Return_list.append([Current[i][1],LastTime[j][2],Current[i][2]],Get_Hostname(Current[i][1]))
	print ("Finish Function Compare_Device_Status")
	return Return_list


if __name__ == '__main__':
	file=open("Line_Notification_Grouplist.txt","r")
	for i in file:
		i=i.split("\n")
		print("Send activate text to : {0}".format(i[0]))
		SendMessage="X1 Notification Activate"
		print(Post_Message_To_LineGroup(i[0],SendMessage,Bot_Authorization))
		DeviceStatusLastTime=[]
		DeviceMonitorLastTime=[]
	try :
		while True:
			print("\n Start Polling Network Device\n")
			DeviceStatusCurrent=Detect_Device_Status()
			print("Device Status Current = {0}".format(DeviceStatusCurrent))
			### Show Result of Monitor Device Status Section ###
			CompareDeviceResult=Compare_Device_Status(Current=DeviceStatusCurrent,LastTime=DeviceStatusLastTime)
			print("Copare result in [IP1,LastTimeStatus,CurentStatus] Format : {0}".format(CompareDeviceResult))
			print("Device Status Lasttime = {0}".format(DeviceStatusLastTime))
			DeviceMonitorCurrent=Detect_Monitor_State(DeviceStatusCurrent) # Detect route and interface change

			print("-----------------------------------------")
			#print (json.dumps(DeviceMonitorCurrent,indent=4))
			print("-----------------------------------------")
			CompareMonitorResult=Compare_Monitor_Status(Current=DeviceMonitorCurrent,LastTime=DeviceMonitorLastTime)
			print("-----------------------------------------")
			print(json.dumps(CompareMonitorResult,indent=4))
			print("-----------------------------------------")
			#Overwrite Last time status
			if(DeviceStatusLastTime==[]):
				SendMessage=tabulate(CompareDeviceResult,headers=[' IP','| Pre-Status  ','| Current Status ','| Hostname'],tablefmt="simple")
				
				file=open("Line_Notification_Grouplist.txt","r")
				for line in file:
					line=line.split("\n")
					print("Send Device Initial Status to : {0}".format(line[0]))
					print(Post_Message_To_LineGroup(line[0],SendMessage,Bot_Authorization))
			elif(CompareDeviceResult!=[]):
				SendMessage="Dear Value Customer , I Detect Network Device Status Change Below :\n"
				for i in range(0,len(CompareDeviceResult)):
					SendMessage+="IP : {0} , Hostname : {3} \n Change Status : \"{1}\" -> \"{2}\" \n".format(CompareDeviceResult[i][0],CompareDeviceResult[i][1],CompareDeviceResult[i][2],CompareDeviceResult[i][3])
				SendMessage+="\n\nThank you and Regard,\n X1\n"
				file=open("Line_Notification_Grouplist.txt","r")
				for line2 in file:
					line2=line2.split("\n")
					print("Send Device Change status to : {0}".format(line2[0]))
					print(Post_Message_To_LineGroup(line2[0],SendMessage,Bot_Authorization))

			if(CompareMonitorResult!=[]):
				SendMessage=""
				SendMessage_Flag=False # True When Sendmessage have vlaue
				SendMessage="\nDear Value Customer , I Detect some concern for you following below : "
				for ResultOneDevice in CompareMonitorResult:
					## Check Interface Error And Discard ##
					SendMessage+="\nIP and Hostname : {0} \\ {1}".format(ResultOneDevice['IP'],ResultOneDevice['Hostname'])
					if(ResultOneDevice['ErrorInterface']!=[]):
						SendMessage_Flag=True
						SendMessage+="\n  Interface Discard/Error :"
						for ResultOneInterface in ResultOneDevice['ErrorInterface']:
							SendMessage+="\n    Interface Name : {0}\n".format(ResultOneInterface['Name'])
							if "in_discard" in ResultOneInterface :
								SendMessage+="      Input Discard : {0} Packets\n".format(ResultOneInterface['Input_discard'])
							if "out_discard" in ResultOneInterface :
								SendMessage+="      Output Discard : {0} Packets\n".format(ResultOneInterface['out_discard'])
							if "in_error" in ResultOneInterface :
								SendMessage+="      Input Error : {0} Packets\n ".format(ResultOneInterface['Input_error'])
							if "out_error" in ResultOneInterface :
								SendMessage+="      Output Error : {0} Packets\n".format(ResultOneInterface['out_error'])
							if "Oper_After" in ResultOneInterface :
								SendMessage+="      Operation status from \"{0}\" to \"{1}\" ".format(ResultOneInterface["Oper_Before"],ResultOneInterface["Oper_After"])
					## Check Config Change ##
					if(ResultOneDevice['Config_Change']!={}):
						SendMessage_Flag=True
						SendMessage+="\n  Configuration Change Notification"
						SendMessage+="\n    Date : {0}".format(ResultOneDevice['Config_Change']['Date'])
						SendMessage+="\n    Time : {0} in GMT+0".format(ResultOneDevice['Config_Change']['Time'])
						SendMessage+="\n    User : {0}".format(ResultOneDevice['Config_Change']['User'])
						if 'CommandList' in ResultOneDevice['Config_Change']:
							SendMessage+="\n    Command List :"
							for Command in ResultOneDevice['Config_Change']['CommandList']:
								SendMessage+="\n      {0}".format(Command)
					## Check Config Save to Startup config ##
					if(ResultOneDevice['Config_Save']==False):
						SendMessage_Flag=True
						SendMessage+="\n  Warning : This Device not save config to Startup-config"
						


				if(SendMessage_Flag):
					print("Send Message compare Monitor : {0}".format(SendMessage))
					file=open("Line_Notification_Grouplist.txt","r")
					for line2 in file:
						line2=line2.split("\n")
						print("Send Summary Device ErrorInterface to : {0}".format(line2[0]))
						print(Post_Message_To_LineGroup(line2[0],SendMessage,Bot_Authorization))
			### End Show Result of Monitor Device Status Section ###
			

			DeviceMonitorLastTime=DeviceMonitorCurrent
			DeviceStatusLastTime=DeviceStatusCurrent
			DeviceMonitorCurrent=[]
			DeviceStatusCurrent=[]
			SendMessage=""
			print("\n Wait 30 Sec For Start Next Polling\n")
			time.sleep(30)
			
	except KeyboardInterrupt :
		print("T-T Bye Bye T-T")
		file2=open("Line_Notification_Grouplist.txt","r")
		for i in file2:
			i=i.split("\n")
			print("Send activate text to : {0}".format(i[0]))
			SendMessage="X1 Notification Deactivate"
			print(Post_Message_To_LineGroup(i[0],SendMessage,Bot_Authorization))
			

