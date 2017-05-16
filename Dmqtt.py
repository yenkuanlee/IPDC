import paho.mqtt.client as mqtt
import os
import json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	client.subscribe("test")
	client.subscribe("Download")
	client.subscribe("DoMap")
	client.subscribe("Buffer")

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def Publish(target,channel,message):
	client = mqtt.Client()
	client.on_publish = on_publish
	client.connect(target, 1883)
	(rc, mid) = client.publish(channel, message, qos=0)

def Download(message):
	# format : Fhash###Fname
	tmp = message.split("###")
	Fhash = tmp[0]
	Fname = tmp[1]
	os.system("timeout 10 ipfs get "+Fhash+" -o /tmp/"+Fname)

RunnerList = list()
def DoMap(message):
	import Map
	global RunnerList
	Jconf = json.loads(message)
	RunnerID = Jconf["RunnerID"]
	RunnerList = Jconf["RunnerList"]
	Mclass = Map.Map(RunnerID,RunnerList)
	Mclass.RunMap()
		
BufferDict = dict()
def Buffer(message):
	global BufferDict
	global RunnerList
	Jmessage = json.loads(message)
	key = Jmessage["key"]
	value = Jmessage["value"]
	if key not in BufferDict:
		BufferDict[key] = list()
	BufferDict[key].append(value)

	if "DoneDone" in BufferDict:
		if len(BufferDict["DoneDone"]) == len(RunnerList):
			print BufferDict
	#if "DoneDone" not in BufferDict:return
	#if BufferDict["DoneDone"] == RunnerList:
	#	print "DoneDone"
	#print BufferDict

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic=='test':
		print str(msg.payload)
	elif msg.topic=="Download":
		Download(str(msg.payload))
	elif msg.topic=="DoMap":
		DoMap(str(msg.payload))
	elif msg.topic=="Buffer":
		#print str(msg.payload)
		Buffer(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
