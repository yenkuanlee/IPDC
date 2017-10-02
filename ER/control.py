import subprocess
import paho.mqtt.client as mqtt
import json
import time
class Control:
	def __init__(self):
		##self.Fname = "fname"
		##self.Fhash = "fhash"
		##self.Chash = "chash"
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
		'''
		# ClusterSpec Upload
		cmd = "timeout 10 ipfs add ClusterSpec.json"
		output = subprocess.check_output(cmd, shell=True)
		tmp = output.split(" ")
		self.Fhash = tmp[1]
		self.Fname = tmp[2].replace("\n","")
		'''
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
                print self.Runner

	'''
	def SetClusterSpec(self):
		f = open('ClusterSpec.conf','r')
		Jspec = ""
		while True:
			line = f.readline()
			if not line:
				break
			try:
				Jspec = json.loads(line)
				break
			except:
				print "Bad ClusterSpec.conf"
				exit(0)

		Wcnt = 0	# worker counter
		for x in Jspec:
			Wcnt += len(Jspec[x])
		self.SetKRunner(Wcnt)	##############################################


		RunnerList = list()
		for x in self.Runner:
			RunnerList.append(x[0]+":2222")

		Rcnt = 0	# Runner counter
		TaskIndex = dict()
		RealSpec = dict()
		for x in Jspec:
			TmpList = list()
			for y in Jspec[x]:
				TmpList.append(RunnerList[Rcnt])
				TaskIndex[RunnerList[Rcnt]] = y	# set index to runner
				Rcnt += 1
			RealSpec[x] = TmpList
		
		print json.dumps(Jspec)
		print json.dumps(RealSpec)

		OutputConf = dict()
		OutputConf["ClusterSpec"] = RealSpec
		OutputConf["TaskIndex"] = TaskIndex
		fw = open('ClusterSpec.json','w')
		fw.write(json.dumps(OutputConf))
		fw.close()

		# default setting
		DefaultJname = ""
		for x in Jspec:
			DefaultJname = x
			break
		fw = open('create_worker.py','w')
		fw.write("import sys\n")
		fw.write("task_number = int(sys.argv[1])\n")
		fw.write("import tensorflow as tf\n")
		fw.write("cluster = tf.train.ClusterSpec("+json.dumps(RealSpec)+")\n")
		fw.write("# You can write yourself below.\n")
		fw.write("server = tf.train.Server(cluster, job_name=\""+DefaultJname+"\", task_index=task_number)\n")
		fw.write("server.start()\n")
		fw.write("server.join()\n")
		fw.close()
	'''
		

	def CallDownload(self):
		if self.Ehash == "ehash":
			print "PLEASE UPLOAD FIRST"
			return
		if len(self.Runner) != 0:
			for x in self.Runner:
				self.Publish(x[0],"DownloadAndSetEnode",self.Ehash+"###enode_setting.py")
		'''
		else:
			f = open("ClusterSpec.json",'r')
			while True:
				line = f.readline()
				if not line:
					break
				try:
					Jline = json.loads(line)
					Tkey = Jline["TaskIndex"].keys()
					for x in Tkey:
						RemoteIP = x.split(":")[0]
						self.Publish(RemoteIP,"Download",self.Fhash+"###"+self.Fname)
						self.Publish(RemoteIP,"Download",self.Chash+"###create_worker.py")
						self.Publish(RemoteIP,"RunCluster",Jline["TaskIndex"][x])
						print Jline["TaskIndex"][x]
				except:
					print "No Good ClusterSpec.json"
					exit(0)
		'''

	def CloseCluster(self):
		if len(self.Runner) != 0:
                        for x in self.Runner:
                                self.Publish(x[0],"CloseCluster","KEVIN")
                else:
                        f = open("ClusterSpec.json",'r')
                        while True:
                                line = f.readline()
                                if not line:
                                        break
                                try:
                                        Jline = json.loads(line)
                                        Tkey = Jline["TaskIndex"].keys()
                                        for x in Tkey:
                                                RemoteIP = x.split(":")[0]
                                                self.Publish(RemoteIP,"CloseCluster","KEVIN")
                                except:
                                        print "No Good ClusterSpec.json"
                                        exit(0)
