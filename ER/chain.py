import control
import ObjectNode
import os
import subprocess
import sys

a = control.Control()

if sys.argv[1] == "start":
	cmd = "ipfs id -f='<id>'"
	peerID = subprocess.check_output(cmd, shell=True)

	a.SetKRunner(int(sys.argv[2]))
	a.DataUpload()
	a.CallDownload()


	b = ObjectNode.ObjectNode(peerID)
	for x in a.Runner:
		node = b.ObjectPeer(x[1])
		b.AddHash(node,"node-"+str(x[2]))
	print b.ObjectHash


	fw = open('Ohash','w')
	fw.write(b.ObjectHash)
	fw.close()

elif sys.argv[1] == "stop":
	cmd = "ipfs swarm peers"
	peers = subprocess.check_output(cmd, shell=True).split("\n")
	PeerIpDict = dict()
	for x in peers:
		if x=="":
			continue
		tmp = x.split("/")
		PeerIpDict[tmp[len(tmp)-1]] = tmp[2]

	import json
	f = open("Ohash","r")
	while True:
		line = f.readline()
		if not line:
			break
		cmd = "ipfs object get "+line
		Jobject = json.loads(subprocess.check_output(cmd, shell=True))
		print Jobject
		Enode = Jobject['Links']
		for x in Enode:
			cmd = "ipfs object get "+x['Hash']
			Jnode = json.loads(subprocess.check_output(cmd, shell=True))
			if Jnode['Data'] in PeerIpDict:
				EnodeIP = PeerIpDict[Jnode['Data']]
				a.Publish(EnodeIP,"CloseEnode","KeepGoing!!!")
	f.close()
	os.system("rm Ohash")
