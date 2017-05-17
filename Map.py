import os
import json
import paho.mqtt.client as mqtt
class Map:
        def __init__(self, JobID, RunnerID, RunnerList):
		self.JobID = JobID
		self.RunnerID = RunnerID
                self.RunnerList = RunnerList
		self.NumberOfRunner = len(RunnerList)
		self.InputPath = 'data.dat'
		
		self.RunnerDict = dict()
		for x in self.RunnerList:
			self.RunnerDict[x[2]] = x[0] # IP
		self.KeyToRunner = dict()

	def on_publish(self, client, userdata, mid):
                print("mid: "+str(mid))

        def Publish(self, target, channel, message):
                client = mqtt.Client()
                #client.on_publish = self.on_publish
                client.connect(target, 1883)
                client.publish(channel, message, qos=0)

	def ThrowKeyValue(self,key,value):
		Jconf = dict()
		Jconf["JobID"] = self.JobID
		Jconf["key"] = key
		Jconf["value"] = value
		if key in self.KeyToRunner:
			self.Publish(self.RunnerDict[self.KeyToRunner[key]],"Buffer",json.dumps(Jconf))
			return
		KeyHash = 0
		for x in key:
			KeyHash += ord(x)
		self.KeyToRunner[key] = KeyHash % self.NumberOfRunner
		self.Publish(self.RunnerDict[self.KeyToRunner[key]],"Buffer",json.dumps(Jconf))

	def RunMap(self):
		f = open(self.InputPath,'r')
		Lcnt = 0
		while True:
			line = f.readline()
			if not line:
				Jconf = dict()
				Jconf["JobID"] = self.JobID
				Jconf["key"] = "DoneDone"
				Jconf["value"] = self.RunnerID
				for x in self.RunnerList:
					self.Publish(x[0],"Buffer",json.dumps(Jconf))
				break
			line = line.replace("\n","")
			Runner = Lcnt % self.NumberOfRunner
			Lcnt += 1
			if Runner != self.RunnerID : continue
			
			# Function Defined by user
			tmp = line.split(" ")
			for x in tmp:
				self.ThrowKeyValue(x,1)
				#os.system("echo '"+x+"' >> output.txt")
