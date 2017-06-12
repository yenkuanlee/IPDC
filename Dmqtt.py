import paho.mqtt.client as mqtt
import os
import json
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	client.subscribe("test")
	client.subscribe("Download", qos=1)
	client.subscribe("DoMap", qos=1)
	client.subscribe("Buffer", qos=1)
	client.subscribe("GetResult", qos=1)
	client.subscribe("CleanUp", qos=1)

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
			client.BufferDict.pop(JobID, None)
			client.JobDict.pop(JobID, None)

def GetResult(message):
	Jmessage = json.loads(message)
	JobID = Jmessage["JobID"]
	Ohash = Jmessage["Ohash"]
	from os import listdir
	if JobID not in listdir("."):
		os.system("mkdir "+JobID)
	os.system("timeout 10 ipfs get "+Ohash+" -o "+JobID)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic=='test':
		print str(msg.payload)
		print client.JobDict
	elif msg.topic=="Download":
		Download(str(msg.payload))
	elif msg.topic=="DoMap":
		DoMap(str(msg.payload))
	elif msg.topic=="Buffer":
		Buffer(str(msg.payload))
	elif msg.topic=="GetResult":
		print str(msg.payload)
		GetResult(str(msg.payload))
	elif msg.topic=="CleanUp":
		print "KEVIN"
		os.system("rm Map.py* Reduce.py* output.txt data.dat")
	#time.sleep(0.01)

client = mqtt.Client()
client.JobDict = dict()
client.BufferDict = dict()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("localhost", 1883, 0)
client.connect_async("localhost", 1883, 0)
client.loop_forever()
