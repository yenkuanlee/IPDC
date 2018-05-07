import subprocess
import paho.mqtt.client as mqtt
import os
import json
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata,flags_dict, rc):
	client.subscribe("test")
	client.subscribe("Download")
	client.subscribe("DoMap")
	client.subscribe("Buffer")
	client.subscribe("GetResult")
	client.subscribe("CleanUp")
	client.subscribe("PortalConnect")

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def Publish(target,channel,message):
	client = mqtt.Client()
	#client.on_publish = on_publish
	client.max_inflight_messages_set(200000)
	client.connect(target, 1883)
	(rc, mid) = client.publish(channel, message, qos=1)
	#time.sleep(0.01)
	print "DMQTT RESULT : "+str(rc)

def Download(message):
	# format : Fhash###Fname
	print "CallDownload : "+message
	tmp = message.split("###")
	Fhash = tmp[0]
	Fname = tmp[1]
	os.system("timeout 10 ipfs get "+Fhash+" -o /tmp/"+Fname)

#RunnerList = list()
###JobDict = dict()
def DoMap(message):
	print "DO MAP MESSAGE : "+message
	import Map
	###global JobDict
	Jconf = json.loads(message)
	RunnerID = Jconf["RunnerID"]
	RunnerList = Jconf["RunnerList"]
	JobID = Jconf["JobID"]
	client.JobDict[JobID] = Jconf
	Mclass = Map.Map(JobID, RunnerID, RunnerList)
	Mclass.RunMap()
		
###BufferDict = dict()
def Buffer(message):
	print "BUFFER MESSAGE : "+message
	#global BufferDict
	#global JobDict
	Jmessage = json.loads(message)
	JobID = Jmessage["JobID"]
	key = Jmessage["key"]
	value = Jmessage["value"]
	if JobID not in client.JobDict:
		time.sleep(1)
		print "You are so lucky"
		Publish("localhost","Buffer",message)
		return
	RunnerList = client.JobDict[JobID]["RunnerList"]
	if JobID not in client.BufferDict:
		client.BufferDict[JobID] = dict()
	if key not in client.BufferDict[JobID]:
		client.BufferDict[JobID][key] = list()
	client.BufferDict[JobID][key].append(value)

	if "DoneDone" in client.BufferDict[JobID]:
		if len(client.BufferDict[JobID]["DoneDone"]) == len(RunnerList): # every runner is done
			# Throw to reduce
			client.BufferDict[JobID].pop("DoneDone", None)
			import Reduce
			print "Start Reduce"
			JobOwner = client.JobDict[JobID]["JobOwner"]
			Rclass = Reduce.Reduce(JobID, JobOwner, client.BufferDict[JobID])
			Rclass.RunReduce()
			print "End Reduce"
			client.BufferDict.pop(JobID, None)
			client.JobDict.pop(JobID, None)

def GetResult(message):
	Jmessage = json.loads(message)
	JobID = Jmessage["JobID"]
	Ohash = Jmessage["Ohash"]
	print "KEVIN RESULT : "+Ohash
	from os import listdir
	if JobID not in listdir("."):
		os.system("mkdir "+JobID)
	os.system("timeout 10 ipfs get "+Ohash+" -o "+JobID)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic=='test':
		print str(msg.payload)
		print client.JobDict
		print client.BufferDict
	elif msg.topic=="Download":
		Download(str(msg.payload))
	elif msg.topic=="DoMap":
		DoMap(str(msg.payload))
	elif msg.topic=="Buffer":
		Buffer(str(msg.payload))
	elif msg.topic=="GetResult":
		print str(msg.payload)
		GetResult(str(msg.payload))
	elif msg.topic=="PortalConnect":
                ConnectIpList = str(msg.payload).split("###")
                for x in ConnectIpList:
                        if x == "":continue
                        cmd = "ipfs swarm connect "+x
                        try:
                                cmd = "ipfs id -f='<id>'"
                                peerID = subprocess.check_output(cmd, shell=True)
                                if peerID in x: # Can't connect to himself
                                        print "\n\nWelcome to be a Domain Portal.\nPlease press Enter!"
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
		print "KEVIN"
		os.system("rm Map.py* Reduce.py* output.txt data.dat")
	#time.sleep(0.01)

client = mqtt.Client()
client.JobDict = dict()
client.BufferDict = dict()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 0)
#client.connect_async("localhost", 1883, 0)
client.loop_forever()
