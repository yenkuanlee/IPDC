import subprocess
import paho.mqtt.client as mqtt
class Control:
	def __init__(self):
		self.Fname = "fname"
		self.Fhash = "fhash"
		self.Mhash = "mhash"
		self.Rhash = "rhash"
		pass
	def on_publish(self, client, userdata, mid):
                print("mid: "+str(mid))
        def Publish(self, target, channel, message):
                client = mqtt.Client()
                client.on_publish = self.on_publish
                client.connect(target, 1883)
                (rc, mid) = client.publish(channel, message, qos=0)
	def DataUpload(self):
		# Data Upload
		cmd = "timeout 10 ipfs add data.dat"
		output = subprocess.check_output(cmd, shell=True)
		tmp = output.split(" ")
		self.Fhash = tmp[1]
		self.Fname = tmp[2].replace("\n","")
		# Map Upload
		cmd = "timeout 10 ipfs add map.py"
		output = subprocess.check_output(cmd, shell=True)
		self.Mhash = output.split(" ")[1]
		# Reduce Upload
		cmd = "timeout 10 ipfs add reduce.py"
		output = subprocess.check_output(cmd, shell=True)
		self.Rhash = output.split(" ")[1]
	'''
	def DataDownload(self):
		if self.Fhash == "fhash":
			print "PLEASE UPLOAD FIRST"
			return
		cmd = "timeout 10 ipfs get "+self.Fhash+" -o kevin.dat"
		output = subprocess.check_output(cmd, shell=True)
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
	def CallDownload(self):
		if self.Fhash == "fhash" or self.Mhash == "mhash" or self.Rhash == "rhash":
			print "PLEASE UPLOAD FIRST"
			return
		Swarm = self.GetSwarm()
		for x in Swarm:
			self.Publish(x,"Download",self.Fhash+"###"+self.Fname)
			self.Publish(x,"Download",self.Mhash+"###map.py")
			self.Publish(x,"Download",self.Rhash+"###reduce.py")
