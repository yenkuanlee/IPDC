import subprocess
from subprocess import Popen
import paho.mqtt.client as mqtt
import os
import json
import time
import threading
import sqlite3

DbPath = "/tmp/.db"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata,flags_dict, rc):
    client.subscribe("test")
    client.subscribe("AskResource")
    client.subscribe("RunningChain")
    client.subscribe("StopChain")
    client.subscribe("DownloadAndSetEnode")
    client.subscribe("SetEnode")
    client.subscribe("AddPeer")
    client.subscribe("KeyStore")
    client.subscribe("CloseEnode")
    client.subscribe("CleanUp")
    client.subscribe("PortalConnect")

def Publish(target,channel,message):
	client = mqtt.Client()
	client.max_inflight_messages_set(200000)
	client.connect(target, 1883)
	(rc, mid) = client.publish(channel, message, qos=1)
	#time.sleep(0.01)
	print("DMQTT RESULT : "+str(rc))

def SetEnode(Eclient):
	print("Setting Enode")
	cmd = "python /tmp/enode_setting.py"
	try:
		p = Popen(cmd.split())
		Eclient.WorkerPID = str(p.pid)
	except Exception as e:
		print("ENODE SETTING ERROR")

def RunVigilante(Eclient):
        print("Run Vigilante")
        cmd = "python /tmp/LocalVigilante.py"
        try:
                p = Popen(cmd.split())
                Eclient.VigilantePID = str(p.pid)
        except Exception as e:
                print("ENODE SETTING ERROR")
		
def DownloadAndSetEnode(message,Eclient):
    # format : Fhash###Fname
    print("CallDownload : "+message)
    tmp = message.split("###")
    Ehash = tmp[0]
    Ohash = tmp[1]
    Vhash = tmp[2]
    os.system("timeout 10 ipfs get "+Ehash+" -o /tmp/enode_setting.py")
    time.sleep(1)
    os.system("timeout 10 ipfs get "+Ohash+" -o /tmp/Ohash")
    time.sleep(1)
    os.system("timeout 10 ipfs get "+Vhash+" -o /tmp/LocalVigilante.py")
    time.sleep(1)
    SEthread = threading.Thread(target=SetEnode, name="SetEnodeAfterDownload", args=(Eclient,))
    SEthread.setDaemon = True
    SEthread.start()
    # Should run LocalVigilante here
    Vthread = threading.Thread(target=RunVigilante, name="RunVigilanteAfterDownload", args=(Eclient,))
    Vthread.setDaemon = True
    Vthread.start()

def LoadDescription():
    Ddict = dict()
    f = open('description.conf','r')
    while True:
        line = f.readline()
        if not line:
                break
        tmp = line.split("=")
        for i in range(len(tmp)):
            if tmp[0] == "description":
                continue
                tmp[i] = tmp[i].replace(" ","")
                tmp[i] = tmp[i].replace("\n","")
                tmp[i] = tmp[i].replace("\t","")
        tmp[0] = tmp[0].lower()
        Ddict[tmp[0]] = tmp[1]
    return Ddict

def AskResource(message):
	print("AskResource : "+message)
	Ddict = json.loads(message)
	# Setup database
	os.system("mkdir -p "+DbPath)
	conn = sqlite3.connect(DbPath+"/chain.db")
	c = conn.cursor()
	c.execute("create table if not exists AskResource(DescriptionHash text, chainName text, chainType text, NumberOfNode text, networkID text, extraData text, rpcport text, description text, PRIMARY KEY(DescriptionHash))")
	conn.commit()
	c.execute("insert into AskResource values('"+Ddict['descriptionhash']+"','"+Ddict['chainname']+"','"+Ddict['chaintype']+"','"+Ddict['numberofnode']+"','"+Ddict['networkid']+"','"+Ddict['extradata']+"','"+Ddict['rpcport']+"','"+Ddict['description']+"')")
	conn.commit()

def RunningChain(message):
	print("RunningChain : "+message)
	conn = sqlite3.connect(DbPath+"/chain.db")
	c = conn.cursor()
	c.execute("create table if not exists RunningChain(Ohash text)")
	conn.commit()
	# insert into RunningChain table
	c.execute("insert into RunningChain values('"+message+"')")
	conn.commit()
	# delete from AskResource table
	cmd = "ipfs object get "+message
	Object = subprocess.check_output(cmd, shell=True)
	JsonObject = json.loads(Object)
	Dhash = "TaiwanNumberOne"
	for x in JsonObject['Links']:
		if x['Name'] == 'description':
			Dhash = x['Hash']
	c.execute("delete from AskResource where DescriptionHash = '"+Dhash+"'")
	conn.commit()

def StopChain(message):
	print("StopChain : "+message)
	conn = sqlite3.connect(DbPath+"/chain.db")
	c = conn.cursor()
	c.execute("delete from RunningChain where Ohash = '"+message+"'")
	conn.commit()

def AddPeer(message):
	print("AddPeer : "+message)
	from web3 import Web3, HTTPProvider
	web3 = Web3(HTTPProvider('http://localhost:8545'))
	try:
		web3.admin.addPeer(message)
	except:
		print("Add Peer Fail!!!")

def KeyStore(message):
    print("KeyStore : "+message)
    tmp = message.split("###")
    try:
        peerID = tmp[0]
        Kname = tmp[1]
        Khash = tmp[2]
    except:
        print("ERROR!!!")
        return
    conn = sqlite3.connect(DbPath+"/chain.db")
    c = conn.cursor()
    try:
        c.execute("create table if not exists keystore(peerID text, Kname text,Khash text, PRIMARY KEY(peerID,Kname))")
        conn.commit()
        c.execute("INSERT OR REPLACE INTO keystore values('"+peerID+"','"+Kname+"','"+Khash+"')")
        conn.commit()
        os.system("timeout 100 ipfs pin add "+Khash)
    except:
        print("Keystore Upsert Error!!!")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic=='test':
        print(str(msg.payload))
    elif msg.topic=="DownloadAndSetEnode":
        DownloadAndSetEnode(str(msg.payload),client)
    elif msg.topic=="SetEnode":
        SEthread = threading.Thread(target=SetEnode, name="SetEnode", args=(client))
        SEthread.setDaemon = True
        SEthread.start()
    elif msg.topic=="AskResource":
        AskResource(str(msg.payload))
    elif msg.topic=="RunningChain":
        RunningChain(str(msg.payload))
    elif msg.topic=="StopChain":
        StopChain(str(msg.payload))
    elif msg.topic=="AddPeer":
        AddPeer(str(msg.payload))
    elif msg.topic=="KeyStore":
        KeyStore(str(msg.payload))
    elif msg.topic=="CloseEnode":
        os.system("kill -9 "+client.WorkerPID)
        os.system("kill -9 "+client.VigilantePID)
        print("KEVIN KILLED "+client.WorkerPID)
        client.WorkerPID = ""
        client.VigilantePID = ""
        os.system("killall -9 geth")
        os.system("rm -rf /tmp/createChain")
    elif msg.topic=="PortalConnect":
        ConnectIpList = str(msg.payload).split("###")
        for x in ConnectIpList:
            if x == "":continue
            cmd = "ipfs swarm connect "+x
            try:
                cmd = "ipfs id -f='<id>'"
                peerID = subprocess.check_output(cmd, shell=True)
                if peerID in x: # Can't connect to himself
                    print("\n\nWelcome to be a Domain Portal.\nPlease press Enter!")
                    continue
                cmd = "ipfs swarm connect "+x
                output = subprocess.check_output(cmd, shell=True)
                if "success" in output:
                    RemoteIP = x.split("/")[2]
                    Publish(RemoteIP,"test","\n\nSuccess to connect with Portal.\nPlease press Enter!")
                    break
            except:
                pass
    elif msg.topic=="CleanUp":
        os.system("rm Map.py* Reduce.py* output.txt data.dat")
        #time.sleep(0.01)

client = mqtt.Client()
client.WorkerPID = ""
client.VigilantePID = ""
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 0)
client.loop_forever()
