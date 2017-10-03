import json
import os
import paho.mqtt.client as paho
import subprocess
import threading
from web3 import Web3, HTTPProvider

chainName = "kevin"
networkID = 9527
extraData = ""
rpcport = 8545

# Load Ohash
Jobject = "INIT"
f = open("Ohash","r")
while True:
        line = f.readline()
        if not line:
                break
        cmd = "timeout 10 ipfs object get "+line
        Jobject = json.loads(subprocess.check_output(cmd, shell=True))
        break

# Download description.conf
Dhash = "INIT"
for x in Jobject:
	if x['Name'] == "description":
		Dhash = x['Hash']
		break
if Dhash != "INIT":
	os.system("timeout 10 ipfs get "+Dhash+" -o /tmp/description.conf")

f = open("description.conf","r")
while True:
	line = f.readline()
	if not line:
		break
	tmp = line.split("=")
	for i in range(len(tmp)):
		tmp[i] = tmp[i].replace(" ","")
		tmp[i] = tmp[i].replace("\t","")
	tmp[0] = tmp[0].lower()
	if tmp[0]=="chainName":
		chainName = tmp[1]
	elif tmp[0]=="networkid":
		networkID = tmp[1]
	elif tmp[0]=="extradata":
		extraData = tmp[1]
	elif tmp[0]=="rpcport":
		rpcport = tmp[1]

def JconfGenerate(networkID,chainName):
        conf = dict()
        conf['chainId'] = networkID
        conf['homesteadBlock'] = 0
        conf['eip155Block'] = 0
        conf['eip158Block'] = 0

        J = dict()
        J['config'] = conf
        J['nonce'] = "0x0000000000000042"
        J['timestamp'] = "0x0"
        J['parentHash'] = "0x0000000000000000000000000000000000000000000000000000000000000000"
        J['extraData'] = "0x0000000000000000000000000000000000000000000000000000000000000000"
        J['gasLimit'] = "0x8000000"
        J['difficulty'] = "0x400"
        J['mixhash'] = "0x0000000000000000000000000000000000000000000000000000000000000000"
        J['coinbase'] = "0x3333333333333333333333333333333333333333"
        J['alloc'] = dict()

        fw = open("./createChain/"+chainName+"/CustomGensis.json",'w')
        fw.write(json.dumps(J))
        fw.close()

os.system("mkdir -p ./createChain/"+chainName)
JconfGenerate(networkID,chainName)
os.system("killall geth")
os.system("geth --networkid \""+str(networkID)+"\" --datadir \"createChain/"+chainName+"\" init ./createChain/"+chainName+"/CustomGensis.json")
os.system("echo \"123\n123\"|geth --datadir \"createChain/"+chainName+"\" account new")

def Estart():
	os.system("/usr/local/bin/geth --mine --minerthreads=4 --datadir \"./createChain/"+chainName+"\" --rpc --rpcport "+str(rpcport)+" --rpcapi \"db,admin,eth,web3,net,personal,miner\" --rpccorsdomain \"*\" --rpcaddr \"0.0.0.0\" --networkid \""+str(networkID)+"\"")


# Start Ethereum
Ethread = threading.Thread(target=Estart, name="Ethread")
Ethread.setDaemon = True
Ethread.start()


# Set Peer
cmd = "timeout 10 ipfs id -f='<id>'"
peerID = subprocess.check_output(cmd, shell=True)
ThisIP = "INIT"
PeerSet = set()
for x in Jobject['Links']:
	NodeHash = x['Hash']
	cmd = "timeout 10 ipfs object get "+NodeHash
	NodePeer = json.loads(subprocess.check_output(cmd, shell=True))['Data']
	if NodePeer == peerID:
		ThisIP = x['Name'].split("###")[1]
	elif "node-" in x['Name'] and "###" and x['Name']:
		PeerSet.add(x['Name'].split("###")[1])


# Add Peer to other nodes
web3 = Web3(HTTPProvider('http://localhost:'+str(rpcport)))
enode = "INIT"
while True:
	try:
		str1 = web3.admin.nodeInfo.enode
		str2 = str1.split("@")
		str3 = str2[1].split(":")
		enode = str2[0]+"@"+ThisIP+":"+str3[len(str3)-1]
		break
	except:
		continue

client = paho.Client()
for x in PeerSet:
	client.connect(x, 1883)
	client.publish("AddPeer", enode, qos=1)

