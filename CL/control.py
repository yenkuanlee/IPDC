import subprocess
import paho.mqtt.client as mqtt
import json
import time
class Control:
	def __init__(self):
		self.Fname = "fname"
		self.Fhash = "fhash"
		self.Chash = "chash"
		self.Runner = set()
		self.JobID = "JobID"

	def on_publish(self, client, userdata, mid):
                print("mid: "+str(mid))

	def Publish(self, target, channel, message):
                client = mqtt.Client()
                #client.on_publish = self.on_publish
		client.max_inflight_messages_set(200000)
                client.connect(target, 1883)
                client.loop_start()
                msg_info = client.publish(channel, message, qos=1)
                if msg_info.is_published() == False:
                        msg_info.wait_for_publish()
                client.disconnect()
                #time.sleep(0.01)

	def DataUpload(self):
		# Data Upload
		cmd = "timeout 10 ipfs add data.dat"
		output = subprocess.check_output(cmd, shell=True)
		tmp = output.split(" ")
		self.Fhash = tmp[1]
		self.Fname = tmp[2].replace("\n","")
		# Map Upload
		cmd = "timeout 10 ipfs add crawler.py"
		output = subprocess.check_output(cmd, shell=True)
		self.Chash = output.split(" ")[1]

	def SetKRunner(self,K):
		# How to choose K good machine...
		# To be continued...
                Rset = set()
                cmd = "ipfs swarm peers"
                output = subprocess.check_output(cmd, shell=True)
                tmp = output.split("\n")
                for i in range(len(tmp)):
			if i >= K or tmp[i]=="": break
                        tmpp = tmp[i].split("/")
                        self.Runner.add((tmpp[2],tmpp[len(tmpp)-1],i)) # format : tuple(IP, NodeID, RunnerID)
                print self.Runner

	def CallDownload(self):
		if self.Fhash == "fhash" or self.Chash == "chash":
			print "PLEASE UPLOAD FIRST"
			return
		for x in self.Runner:
			self.Publish(x[0],"Download",self.Fhash+"###"+self.Fname)
			self.Publish(x[0],"Download",self.Chash+"###crawler.py")

	def CallRun(self):
                RunnerList = list(self.Runner)
                cmd = "ipfs id -f='<id>'"
                JobOwner = subprocess.check_output(cmd, shell=True)
                JobID = str(int(time.time()))
		for x in self.Runner:
                        Jconf = dict()
                        Jconf["RunnerList"] = RunnerList
                        Jconf["RunnerID"] = x[2]
                        Jconf["JobOwner"] = JobOwner
                        Jconf["JobID"] = JobID
                        self.JobID = JobID
                        self.Publish(x[0],"DoCrawler",json.dumps(Jconf))
                        print "KEVIN CALL CRAWLER"
                        print json.dumps(Jconf)

	def CheckResult(self):
		from os import listdir
		while True:
			Check = listdir("/tmp")
			if self.JobID not in Check:continue
			F = listdir("/tmp/"+self.JobID)
			if len(F) == len(self.Runner):
				print "Done"
				break
			#time.sleep(0.1)
