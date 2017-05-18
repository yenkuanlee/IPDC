import os
import time
import json
import subprocess
import paho.mqtt.client as mqtt
class Reduce:
        def __init__(self, JobID,JobOwner, BufferDict):
		self.JobID = JobID
		self.JobOwner = JobOwner
		self.BufferDict = BufferDict
		self.ResultDict = dict()

	def on_publish(self, client, userdata, mid):
                print("mid: "+str(mid))

        def Publish(self, target, channel, message):
                client = mqtt.Client()
                #client.on_publish = self.on_publish
                client.connect(target, 1883)
                msg_info = client.publish(channel, message, qos=1)
		#msg_info.wait_for_publish()
		time.sleep(0.01)

	def GetOwnerIP(self):
		cmd = "ipfs swarm peers"
		output = subprocess.check_output(cmd, shell=True)
		tmp = output.split("\n")
		for x in tmp:
			if x == "":continue
			tmpp = x.split("/")
			if tmpp[len(tmpp)-1] == self.JobOwner:
				return tmpp[2]
		return "ERROR"
		
	def ThrowKeyValue(self, key, value):
                self.ResultDict[key] = value
                if self.ResultDict.keys() == self.BufferDict.keys():
                        f = open("output.txt","w")
                        for x in self.ResultDict:
                                f.write(x+"\t"+self.ResultDict[x]+"\n")
                        f.close()
                        cmd = "ipfs add output.txt"
                        output = subprocess.check_output(cmd, shell=True)
                        Ohash = output.split(" ")[1]
                        OwnerIP = self.GetOwnerIP()
			Jconf = dict()
			Jconf["Ohash"] = Ohash
			Jconf["JobID"] = self.JobID
                        self.Publish(OwnerIP,"GetResult",json.dumps(Jconf))
			self.Publish("localhost","CleanUp","")

	def reduce(self,key,ValueList):
		# Defined by user
		cnt = 0
		for x in ValueList:
			cnt += x
		self.ThrowKeyValue(key, str(cnt))

	def RunReduce(self):
		for key in self.BufferDict:
			self.reduce(key, self.BufferDict[key])
