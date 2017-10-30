import json
import paho.mqtt.client as mqtt
import sqlite3
import subprocess
from web3 import Web3, HTTPProvider
class Control:
	def __init__(self):
		# Path setting
		self.Fpath = "/tmp"
		self.DbPath = "/tmp/.db"
		# Web3 setting
		self.web3 = Web3(HTTPProvider('http://localhost:8545'))
		# DB setting
		self.conn = sqlite3.connect(self.DbPath+"/FileSign.db")
		self.c = self.conn.cursor()
		self.c.execute("create table if not exists AccountEhash(account text, Ehash text, PRIMARY KEY(account))")
                self.conn.commit()
		self.c.execute("create table if not exists SendLog(account text, Thash text)")
		self.conn.commit()
		self.c.execute("create table if not exists SignFhash(SignHash text, Fhash text, PRIMARY KEY(SignHash))")
		self.conn.commit()
		try:
			self.c.execute("insert into AccountEhash values ('admin','"+str(self.web3.eth.coinbase)+"')")
			self.conn.commit()
		except:
			pass
	def Publish(self, target, channel, message):
                client = mqtt.Client()
                client.max_inflight_messages_set(200000)
                client.connect(target, 1883)
                client.loop_start()
                msg_info = client.publish(channel, message, qos=1)
                if msg_info.is_published() == False:
                        msg_info.wait_for_publish()
                client.disconnect()
	def AccountNew(self, account, passwd):
		Eflag = False
		OldEhash = self.GetEhash(account)
		if OldEhash != "ERROR":
			Eflag = True
		self.c.execute("create table if not exists AccountEhash(account text, Ehash text, PRIMARY KEY(account))")
		self.conn.commit()
		if Eflag:
			print "account already existed!!!"
			return
		Ehash = self.web3.personal.newAccount(passwd)
		self.c.execute("insert into AccountEhash values('"+account+"','"+Ehash+"')")
		self.conn.commit()
		print "New Account : "+account
	def GetEhash(self,account):
		try:
			Ehash = self.c.execute("select Ehash from AccountEhash where account = '"+account+"'")
			for x in Ehash:
				return x[0]
		except:
			pass
		return "ERROR"
	def AccountUnlock(self, account, passwd):
		Ehash = self.GetEhash(account)
		self.web3.personal.unlockAccount(Ehash, passwd)
	def FileUpload(self,Fname):
		cmd = "ipfs add "+self.Fpath+"/"+Fname
		try:
			Fhash = subprocess.check_output(cmd, shell=True).split(" ")[1]
			return Fhash
		except:
			print "FILE ERROR!"
			exit(0)
			#return "ERROR"
	def FileSign(self, account, passwd, Fname):
		Ehash = self.GetEhash(account)
		Fhash = self.FileUpload(Fname)
		self.AccountUnlock(account,passwd)
		SignHash = self.web3.eth.sign(Ehash, text = Fhash)
		self.c.execute("insert into SignFhash values('"+SignHash+"','"+Fhash+"')")
		self.conn.commit()
		return SignHash
	def SendFile(self, account, passwd, Fname, ToAccount):
		FromEhash = self.GetEhash(account)
		ToFhash = self.GetEhash(ToAccount)
		SignHash = self.FileSign(account, passwd, Fname)
		#print {'to': str(ToFhash), 'from': FromEhash, 'data':SignHash}
		Thash = self.web3.eth.sendTransaction({'to': ToFhash, 'from': FromEhash, 'value': 1, 'data':SignHash})
		self.c.execute("insert into SendLog values('"+ToAccount+"','"+Thash+"')")
		self.conn.commit()
		return Thash
	def GetThash(self,account):
		Thash = self.c.execute("select Thash from SendLog where account = '"+account+"'")
		for x in Thash:
			return x[0]
		return "ERROR"
	def GetSignHash(self,Thash):
		Tdict = self.web3.eth.getTransaction(Thash)
		return (Tdict['from'],Tdict['to'],Tdict['input'])
	def Varify(self,account,passwd,ToAccount,Fname):
		FromEhash = self.GetEhash(account)
		ToEhash = self.GetEhash(ToAccount)
		SignHashSet = set()
		Thash = self.c.execute("select Thash from SendLog where account = '"+ToAccount+"'")
		for x in Thash:
			tmp = self.GetSignHash(x[0])
			if tmp[0]!=FromEhash or tmp[1]!=ToEhash:
				continue
			SignHashSet.add(tmp[2])
		Fsign = self.FileSign(account, passwd, Fname)
		if Fsign in SignHashSet:
			return True
		return False
	def GetFhash(self,account):
		Thash = self.GetThash(account)
		SignHash = self.GetSignHash(Thash)
		Fhash = self.c.execute("select Fhash from SignFhash where SignHash = '"+SignHash[2]+"'")
		for x in Fhash:
			return x[0]
		return "ERROR"
