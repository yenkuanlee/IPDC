import paho.mqtt.client as mqtt
import os


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	client.subscribe("test")
	client.subscribe("Download")

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def Publish(target,channel,message):
	client = mqtt.Client()
	client.on_publish = on_publish
	client.connect(target, 1883)
	(rc, mid) = client.publish(channel, message, qos=0)

def Download(message):
	tmp = message.split("###")
	Fhash = tmp[0]
	Fname = tmp[1]
	os.system("timeout 10 ipfs get "+Fhash+" -o /tmp/"+Fname)
		
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic=='test':
		print str(msg.payload)
	elif msg.topic=="Download":
		Download(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
