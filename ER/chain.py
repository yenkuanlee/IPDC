import control
import ObjectNode
import os
import subprocess
import sys

AskResource = True
DbPath = "/tmp/.db"

a = control.Control()
def LoadDescription():
    Ddict = dict()
    f = open('description.conf','r')
    while True:
        line = f.readline()
        if not line:
                break
        tmp = line.split("=")
        for i in range(len(tmp)):
		if tmp[0] == "description":
                        continue
                tmp[i] = tmp[i].replace(" ","")
                tmp[i] = tmp[i].replace("\n","")
                tmp[i] = tmp[i].replace("\t","")
        tmp[0] = tmp[0].lower()
        Ddict[tmp[0]] = tmp[1]
    return Ddict

if sys.argv[1] == "ask_resource": ### for iServChain
	import json
	# Get description.conf hash
	cmd = "timeout 10 ipfs add description.conf"
	DescriptionHash = "INIT"
	try:
		DescriptionHash = subprocess.check_output(cmd, shell=True).split(" ")[1]
	except:
		print "Bad description.conf.\nAsk for resource failed."
		exit(0)
	# Get Description dictionary
	Ddict = LoadDescription()
	Ddict['descriptionhash'] = DescriptionHash
	# Get all peer ip
	cmd = "ipfs swarm peers"
        peers = subprocess.check_output(cmd, shell=True).split("\n")
        PeerIpSet = set()
        for x in peers:
                if x=="":
                        continue
                tmp = x.split("/")
		PeerIpSet.add(tmp[2])
	for x in PeerIpSet:
		a.Publish(x,"AskResource",json.dumps(Ddict))
	
elif sys.argv[1] == "start":
	# Get PeerID
	cmd = "timeout 10 ipfs id -f='<id>'"
	peerID = subprocess.check_output(cmd, shell=True)
	# Get description.conf Hash
	cmd = "timeout 10 ipfs add description.conf"
	description = subprocess.check_output(cmd, shell=True).split(" ")[1]
	# Get information of description.conf
        DescriptionDict = LoadDescription()
	### In the future, we will publish a consent to IPFS in here.
        ### Resource owner can agree to contribute and download the consent.
        ### Then we can use "ipfs dht findprovs" to find K runners who had download the consenr.
        ### The Runner information will record to ipfs object.
	try:
	    if not AskResource:
            	a.SetKRunner(int(DescriptionDict['numberofnode']))
	    else:
	    	a.SetKAgreementRunner(description,int(DescriptionDict['numberofnode']))
	    	if len(a.Runner) < int(DescriptionDict['numberofnode']):
			print "Not enough resource to build chain. Please wait..."
			exit(0)
        except:
            print "Bad Description.conf without 'NumberOfNode' !"
            exit(0)
	# Generate Object Node
	b = ObjectNode.ObjectNode(peerID)
	for x in a.Runner:
		node = b.ObjectPeer(x[1])
		b.AddHash(node,"node-"+str(x[2])+"###"+str(x[0]))
	b.AddHash(description,"description")
	# write Ohash to Local
	fw = open('Ohash','w')
	fw.write(b.ObjectHash)
	fw.close()
	# Upload code and call download
	a.DataUpload()
        a.CallDownload()
	# Publish Ohash to db
	cmd = "ipfs swarm peers"
	peers = subprocess.check_output(cmd, shell=True).split("\n")
        PeerIpSet = set()
        for x in peers:
                if x=="":
                        continue
                tmp = x.split("/")
		try:
                	PeerIpSet.add(tmp[2])
		except:
			pass
	for x in PeerIpSet:
		a.Publish(x,"RunningChain",b.ObjectHash)

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
	os.system("rm Ohash *.pyc")
