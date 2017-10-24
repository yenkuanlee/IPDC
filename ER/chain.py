import control
import json
import ObjectNode
import os
import subprocess
import sys
import time

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
	try:
        	for i in range(len(tmp)):
			if tmp[0] == "description":
				tmp[i] = tmp[i].replace("\n","")
                        	continue
                	tmp[i] = tmp[i].replace(" ","")
                	tmp[i] = tmp[i].replace("\n","")
                	tmp[i] = tmp[i].replace("\t","")
        	tmp[0] = tmp[0].lower()
        	Ddict[tmp[0]] = tmp[1]
	except:
		continue
    return Ddict

if sys.argv[1] == "ask_resource": ### for iServChain
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

	StopOhash = "TaiwanNumberOne"
	f = open("Ohash","r")
	while True:
		line = f.readline()
		if not line:
			break
		StopOhash = line
		cmd = "ipfs object get "+StopOhash
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
	# sent message to delete Ohash from db
	for x in PeerIpDict:
		a.Publish(PeerIpDict[x],"StopChain",StopOhash)
	os.system("rm Ohash *.pyc")

elif sys.argv[1] == "add_node":
	AddNumber = int(sys.argv[2])
	# Load Ohash
	OldOhash = "INIT"
	f = open('Ohash','r')
	while True:
		line = f.readline()
		if not line:
			break
		cmd = "timeout 10 ipfs object get "+line
		Jnode = json.loads(subprocess.check_output(cmd, shell=True))
		OldOhash = line
		break
	# Load old node
	OldNode = set()
	for x in Jnode['Links']:
		if "node-" in x['Name']:
			OldNode.add(x['Name'].split("###")[1])
	# Update description
	Ddict = LoadDescription()
	Ddict['numberofnode'] = str(int(Ddict['numberofnode']) + AddNumber)
	fw = open('description.conf','w')
	for x in Ddict:
		fw.write(x+" = "+Ddict[x]+"\n")
	fw.close()
	# Upload description
	cmd = "timeout 10 ipfs add description.conf"
	DescriptionHash = "INIT"
	try:
		DescriptionHash = subprocess.check_output(cmd, shell=True).split(" ")[1]
	except:
		print "Bad description.conf.\nAsk for resource failed."
		exit(0)
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
		if x in OldNode:
			continue
		a.Publish(x,"AskResource",json.dumps(Ddict))
	# Check Runner
	CheckRunnerCnt = 0
	while True:
		try:
			CheckRunnerCnt += 1
        		if not AskResource:
				pass
                		#a.SetKRunner(int(DescriptionDict['numberofnode']))
            		else:
                		a.SetKAgreementRunner(DescriptionHash,AddNumber)
                		if len(a.Runner) < AddNumber:
                        		print "waiting ...("+str(CheckRunnerCnt)+")"
					time.sleep(1)
				else:
					break
        	except:
            		print "Bad Description.conf without 'NumberOfNode' !"
            		exit(0)
	# Set ObjectNode
	b = ObjectNode.ObjectNode(Jnode['Data'])
	NodeCnt = 0
	for x in Jnode['Links']:
		if "node-" not in x['Name']:
			continue
		b.AddHash(x['Hash'],x['Name'])
		NodeCnt += 1
	for x in a.Runner:
		node = b.ObjectPeer(x[1])
		b.AddHash(node,"node-"+str(NodeCnt)+"###"+str(x[0]))
		NodeCnt += 1
	b.AddHash(DescriptionHash,"description")
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
	for x in PeerIpSet:
		a.Publish(x,"StopChain",OldOhash)
