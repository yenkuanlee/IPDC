# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import json
import urllib2
import paho.mqtt.client as mqtt
import subprocess
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

class Crawler:
	def __init__(self, JobID, RunnerID, RunnerList, JobOwner):
		self.fw = open('output.txt','w')
                self.JobID = JobID
                self.RunnerID = RunnerID
		self.JobOwner = JobOwner
                self.RunnerList = RunnerList
                self.NumberOfRunner = len(RunnerList)
                self.InputPath = 'data.dat'

                self.RunnerDict = dict()
                for x in self.RunnerList:
                        self.RunnerDict[x[2]] = x[0] # IP
                self.KeyToRunner = dict()

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

	def ResultUpload(self):
                cmd = "ipfs add output.txt"
                output = subprocess.check_output(cmd, shell=True)
                Ohash = output.split(" ")[1]
                OwnerIP = self.GetOwnerIP()
                Jconf = dict()
                Jconf["Ohash"] = Ohash
                Jconf["JobID"] = self.JobID
                self.Publish(OwnerIP,"GetResult",json.dumps(Jconf))
                time.sleep(0.01)
                #self.Publish("localhost","CleanUp","")
                return

	def crawler(self,info):
		url = ""
		if "http" in info:
			url = info
		else:
			url = "http://www.gomaji.com/"+info+".html"

		response = urllib2.urlopen(url)
		page_source = response.read()
		Cflag = False
		tmp = page_source.split("<script type=\"application/ld+json\">")[1].split("</script>")[0]
		Rdict = dict()
		tmpp = tmp.split("\n")
		for x in tmpp:
			if "\"name\"" in x:
				Rdict['name'] = x.split("\"")[3].split(" - GOMAJI")[0]
			elif "\"productID\"" in x:
				Rdict['productID'] = x.split("\"")[3]
			elif "\"image\"" in x:
				Rdict['image'] = x.split("\"")[3]
			elif "\"description\"" in x:
				Rdict['description'] = x.split("\"")[3]
			elif "\"url\"" in x:
				Rdict['url'] = x.split("\"")[3]
			elif "\"price\"" in x:
				Rdict['price'] = x.split("\"")[3]
		self.fw.write("{\n")
		for x in Rdict:
			self.fw.write(x+" : "+Rdict[x]+"\n")
		self.fw.write("}\n")

	def Run(self):
		#self.fw.write("[\n")
		f = open(self.InputPath,'r')
		Lcnt = 0
		while True:
			line = f.readline()
			if not line : break
			line = line.replace("\n","")
			try:
				Runner = Lcnt % self.NumberOfRunner
				Lcnt += 1
				if Runner != self.RunnerID : continue
				self.crawler(line)
			except:
				continue
		#self.fw.write("]\n")
		self.fw.close()
		self.ResultUpload()
