import subprocess
import paho.mqtt.client as mqtt
import json
import time
class Control:
	def __init__(self):
		self.Ehash = "ehash"
		self.Runner = set()
		self.JobID = "JobID"

	def Publish(self, target, channel, message):
                client = mqtt.Client()
		client.max_inflight_messages_set(200000)
                client.connect(target, 1883)
                client.loop_start()
                msg_info = client.publish(channel, message, qos=1)
                if msg_info.is_published() == False:
                        msg_info.wait_for_publish()
                client.disconnect()

	def DataUpload(self):
		# Enode_Setting Upload
		cmd = "timeout 10 ipfs add enode_setting.py"
		output = subprocess.check_output(cmd, shell=True)
		self.Ehash = output.split(" ")[1]

	'''
	def GetSwarm(self):
		Rset = set()
		cmd = "ipfs swarm peers"
		output = subprocess.check_output(cmd, shell=True)
		tmp = output.split("\n")
		for x in tmp:
			if x=="":continue
			Rset.add(x.split("/")[2])
		return Rset
	'''

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

	def CallDownload(self):
		if self.Ehash == "ehash":
			print "PLEASE UPLOAD FIRST"
			return
		if len(self.Runner) != 0:
			for x in self.Runner:
				self.Publish(x[0],"DownloadAndSetEnode",self.Ehash+"###enode_setting.py")

	def CloseCluster(self):
		if len(self.Runner) != 0:
                        for x in self.Runner:
                                self.Publish(x[0],"CloseCluster","KEVIN")
