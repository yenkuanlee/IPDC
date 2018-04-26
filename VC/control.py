import subprocess
import paho.mqtt.client as mqtt
import json
import time
import os
class Control:
	def __init__(self):
		self.Runner = set()

	def Publish(self, target, channel, message):
                client = mqtt.Client()
		client.max_inflight_messages_set(200000)
                client.connect(target, 1883)
                client.loop_start()
                msg_info = client.publish(channel, message, qos=1)
                if msg_info.is_published() == False:
                        msg_info.wait_for_publish()
                client.disconnect()

	def SetKRunner(self,K):
		# How to choose K good machine...
		# To be continued...
		K = K-1 # i am one of K
		try:
			f = open('runner.json','r')
			line = f.readline()
			Jline = json.loads(line)
			if len(Jline)!=0:
				self.Runner = set(Jline)
				return
		except:
			pass
                Rset = set()
                cmd = "ipfs swarm peers"
                output = subprocess.check_output(cmd, shell=True)
                tmp = output.split("\n")
                for i in range(len(tmp)):
			if i >= K or tmp[i]=="": break
                        tmpp = tmp[i].split("/")
                        self.Runner.add((tmpp[2],tmpp[len(tmpp)-1],i)) # format : tuple(IP, NodeID, RunnerID)
		fw = open('runner.json','w')
                fw.write(json.dumps(list(self.Runner)))
		fw.close()


	def VoltDBDaemon(self,host,port,hostcount):
		os.system("rm -rf volt*")
		os.system("/home/localadmin/voltdb/bin/voltdb init")
		cmd = "/home/localadmin/voltdb/bin/voltdb start --http=localhost:"+port+" -c "+hostcount+" -H "+host+" -B"
		os.system(cmd)
		print "waiting voltdb daemon..."
		time.sleep(5)
		for x in self.Runner:
			self.Publish(x[0],"RunCluster",host+"###"+port+"###"+hostcount)
		print "waiting for worker setting..."
		time.sleep(10)
		print "done!"
		time.sleep(1)
		


	def CloseCluster(self):
		os.system("/home/localadmin/voltdb/bin/voltadmin shutdown")
		os.system("rm runner.json")
