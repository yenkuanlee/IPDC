from web3 import Web3, HTTPProvider
web3 = Web3(HTTPProvider('http://localhost:8545'))

# 0xee5ed742a852cac6045a4f29382279867d3aac95    admin
# 0x58f5fe961d419e4cffd40410aa1c4f0250bcc89f    kevin99
# 0x865707e28f646756874ff59f0b1b64b7b490f2c4    kevin98


# admin give money
#web3.personal.unlockAccount("0xee5ed742a852cac6045a4f29382279867d3aac95","123")
#web3.eth.sendTransaction({"to": "0x58f5fe961d419e4cffd40410aa1c4f0250bcc89f", "from": "0xee5ed742a852cac6045a4f29382279867d3aac95","value":web3.toWei("100", "ether")})
#print web3.fromWei(web3.eth.getBalance("0x58f5fe961d419e4cffd40410aa1c4f0250bcc89f"), "ether")

# kevin99 to kevin98
#web3.personal.unlockAccount("0x58f5fe961d419e4cffd40410aa1c4f0250bcc89f","123")
#web3.eth.sendTransaction({"to": "0x865707e28f646756874ff59f0b1b64b7b490f2c4", "from": "0x58f5fe961d419e4cffd40410aa1c4f0250bcc89f","value":web3.toWei("1", "ether")})

#print web3.fromWei(web3.eth.getBalance("0x58f5fe961d419e4cffd40410aa1c4f0250bcc89f"), "ether")
#print web3.fromWei(web3.eth.getBalance("0x865707e28f646756874ff59f0b1b64b7b490f2c4"), "ether")


# test private key
print web3.personal.importRawKey("58f5fe961d419e4cffd40410aa1c4f0250bcc89f","123")
