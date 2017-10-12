import json
from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider('http://localhost:8545'))
print json.dumps(web3.admin.peers)
#print json.dumps(Jpeer)
