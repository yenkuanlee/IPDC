import os

chainName = "kevin"
networkID = 9527
extraData = ""
rpcport = 9528

def JconfGenerate(networkID,chainName):
        import json
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

os.system("mkdir -p ./createChain/kevin")
JconfGenerate(networkID,chainName)
os.system("killall geth")
os.system("geth --networkid \""+str(networkID)+"\" --datadir \"createChain/"+chainName+"\" init ./createChain/"+chainName+"/CustomGensis.json")
os.system("echo \"123\n123\"|geth --datadir \"createChain/"+chainName+"\" account new")

os.system("/usr/bin/geth --mine --minerthreads=4 --datadir \"./createChain/"+chainName+"\" --rpc --rpcport "+str(rpcport)+" --rpcapi \"db,admin,eth,web3,net,personal,miner\" --rpccorsdomain \"*\" --rpcaddr \"0.0.0.0\" --networkid \""+str(networkID)+"\"")
