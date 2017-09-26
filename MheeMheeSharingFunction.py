import sys
import base64
import subprocess

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
    print("Start Ping function ")
    print(" Popen ="+'ping -n 2 -w 1 ' + hostname)
    p = subprocess.Popen('ping -n 2 -w 1 ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pingStatus = 'ok';
        
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
        #print(" Output = {0}".format(output))  
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
        if(output.endswith('TTL expired in transit.')):
            pingStatus = 'TTL Expire'
            break
        #end if
    #endFor
    return pingStatus
#endDef    

def Add_Device(Command=""):
    print("Start Add_Device Function")
    if(Command[2].lower()=="netconf"):
        file = open("Netconf Credential.txt","a")
    elif(Command[2].lower()=="prime"):
        file = open("API Credential.txt","a")
    elif(Command[2].lower()=="apic-em"):
        file = open("API Credential.txt","a")
    else:
        return "Fail to Open File After : not have stroage in command"

    line="\n"+Command[3]+" "+Command[4]+" "+Command[5]+" "+Command[6]

    try:
        file.write(line)
        print("End Add_Device Function with success output")
        return "Success"
    except:
        print("End Add_Device Function with fail output")
        return "Fail"

def List_Device(Command=""):
    OutputMessage="Result of Device List in File"
    OutputMessage+="\n---------------------------------\n"
    Number=0
    print("Start Add_Device Function")
    if(Command[2].lower()=="netconf"):
        file = open("Netconf Credential.txt","r")
    elif(Command[2].lower()=="prime"):
        file = open("API Credential.txt","r")
    elif(Command[2].lower()=="apic-em"):
        file = open("API Credential.txt","r")
    else:
        return "Fail to Open File After : not have stroage in command"

    for line in file:
        Number+=1
        temp=line.split()
        print(temp)
        OutputMessage+="\nNo. "+str(Number)
        OutputMessage+="\n IP Address and port: "+temp[0]+":"+temp[1]
        OutputMessage+="\n Username/Password : "+temp[2]+"/"+temp[3]
    return OutputMessage+"\n---------------------------------\n"
