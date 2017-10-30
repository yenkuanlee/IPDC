import os
import subprocess
from subprocess import Popen
import sys
import threading
import time

def Publish(target, channel, message):
	import paho.mqtt.client as mqtt
	Pclient = mqtt.Client()
        Pclient.max_inflight_messages_set(200000)
        Pclient.connect(target, 1883)
        Pclient.loop_start()
        msg_info = Pclient.publish(channel, message, qos=1)
        #if msg_info.is_published() == False:
        #        msg_info.wait_for_publish()
        Pclient.disconnect()

def KillProcess(process):
	try:
                f = open('.ipfs/'+process+'.pid','r')
                while True:
                        line = f.readline()
                        if not line:
                                break
                        line = line.replace("\n","")
                        os.system("kill -9 "+line)
                        os.system("echo '' > .ipfs/"+process+".pid")
        except:
                pass

def IpfsDaemon():
	cmd = "ipfs daemon"
        try:
            p = Popen(cmd.split(),stdout=subprocess.PIPE)
	    time.sleep(2)
            #os.system("echo "+str(p.pid)+" > .ipfs/ipfs.pid")
	    fw = open('.ipfs/ipfs.pid','w')
            fw.write(str(p.pid))
            fw.close()
	    while True:
		line = p.stdout.readline().replace("\n","")
		if "Daemon is ready" == line:
			print "IPDC is ready!\n"
			break
        except Exception as e:
            print "CREATE WORKER ERROR"

def DmqttDaemon(project):
	Npath = os.getcwd()
	os.system("cp "+project+"/Dmqtt.py /tmp")
	os.chdir("/tmp")
        cmd = "python Dmqtt.py"
        try:
            p = Popen(cmd.split())
	    os.chdir(Npath)
            #os.system("echo "+str(p.pid)+" > .ipfs/dmqtt.pid")
	    fw = open('.ipfs/dmqtt.pid','w')
            fw.write(str(p.pid))
            fw.close()
        except Exception as e:
            print "CREATE WORKER ERROR"

# read config
f = open('ipdc.conf','r')
Cdict = dict()
while True:
	line = f.readline()
	if not line:
		break
	line = line.split("#")[0] # so we can add commands in conf
	tmp = line.split("=")
	for i in range(len(tmp)):
		tmp[i] = tmp[i].replace(" ","")
		tmp[i] = tmp[i].replace("\n","")
		tmp[i] = tmp[i].replace("\t","")
	try:
		Cdict[tmp[0].upper()] = tmp[1]
	except:
		pass
f.close()
try:
	Cdict["DOMAIN_NAME"] = Cdict["PROJECT"]+"-"+Cdict["DOMAIN_NAME"]
	# add information of project name to domain name
except:
	print "Somthing wrong in ipdc.conf !!!"
	exit(0)

if sys.argv[1] == "init":
	# install mqtt and paho
	print "Installing MQTT..."
	os.system("sudo apt-get install python-pip python-dev -y")
	os.system("sudo apt-get install mosquitto mosquitto-clients -y")
	os.system("sudo service mosquitto restart")
	os.system("sudo pip install paho-mqtt")
	print "Installing tensorflow CPU version..."
	os.system("sudo pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.3.0-cp27-none-linux_x86_64.whl")
	print "Setting ethereum..."
	os.system("sudo cp .ipfs/geth /usr/local/bin")
	os.system("sudo -H pip install --upgrade pip")
	os.system("sudo pip install web3")
	print "done."

if sys.argv[1] == "stop":
	# check if you are a worker
	cmd = "pgrep -f 'create_worker.py'"
	output = subprocess.check_output(cmd, shell=True).split("\n")
	print "Checking process...\n"
	time.sleep(1)
	output2 = subprocess.check_output(cmd, shell=True).split("\n")
	Check = (set(output).intersection(output2))-{''}
	if len(Check) > 0:
		flag = True
		cnt = 0
		while(flag):
			cnt += 1
			YN = raw_input( "You are being someone's woker.\nAre you sure you want to leave? (yes|no)... \n")
			if YN.lower() == "no":
				print "\nIPDC still running.\n"
				exit(0)
			elif YN.lower() == 'yes':
				print "\nClosing IPDC.\n"
				flag = False
			else:
				if cnt == 3:
					print "Don't try to play me...\nBye!"
					exit(0)
				print "Please input again (yes|no)."
				time.sleep(1)

	os.system("pkill -f 'create_worker.py'")
	KillProcess("ipfs")
	KillProcess("dmqtt")
	os.system("rm -rf .ipfs/*.pid")
	os.system("rm -rf /tmp/.db")
	os.system("rm /tmp/Dmqtt.py /tmp/Ohash /tmp/createChain /tmp/description.conf /tmp/enode_setting.py")
	print "done."

elif sys.argv[1] == "start":
	# set ipfs
	os.system("sudo rm -rf /usr/local/bin/ipfs")
	os.system("sudo cp .ipfs/ipfs /usr/local/bin")
	os.system("sudo chmod 777 /usr/local/bin/ipfs")
	os.system("sudo rm -rf /opt/iservstor/conf/iservstor.conf")
	os.system("sudo mkdir -p /opt/iservstor/conf")
	os.system("sudo touch /opt/iservstor/conf/iservstor.conf")
	os.system("sudo chmod 777 /opt/iservstor/conf/iservstor.conf")
	fw = open('/opt/iservstor/conf/iservstor.conf','w')
	for x in Cdict:
		fw.write(x+" = "+Cdict[x]+"\n")
	fw.close()
	os.system("sudo chmod 755 /opt/iservstor/conf/iservstor.conf")
	os.system("rm -rf ~/.ipfs")
	os.system("ipfs init")
	os.system("ipfs config Addresses.Gateway /ip4/127.0.0.1/tcp/8082")
	KillProcess("ipfs")
	###IpfsDaemon()
	Ithread = threading.Thread(target=IpfsDaemon, name='T1')
        Ithread.start()

	# start dmqtt
	KillProcess("dmqtt")
	DmqttDaemon(Cdict["PROJECT"])
	
	# ask portal to connect
	###cmd = "ipfs id -f='<addrs>'"
	###output = subprocess.check_output(cmd, shell=True).split("\n")
	output = list()
        cnt = 0
        while True:
		flag = False
		try:
                	cmd = "ipfs id -f='<addrs>'"
                	output = subprocess.check_output(cmd, shell=True).split("\n")
		except:
			time.sleep(1)
			continue
                for x in output:
                        if "/ip4/" in x:
                                flag = True
                                break
                if flag:
                        break
                time.sleep(1)
                cnt += 1
                if cnt > 5:
                        print "IPFS ERROR!"
                        exit(0)
	
	ConnectSet = set()
	for x in output:
		if "/ip4/" not in x: # portal only connect with ip4
			continue
		elif "/127.0.0.1/" in x: # localhost no use and need not to publish
			continue
		ConnectSet.add(x)
	X = ""
	for x in ConnectSet:
		X += x+"###"
	try:
		if Cdict["MANAGEMENT_IP"] in X:
			print "Welcome to be a IPDC Domain Portal."
		else:
			Publish(Cdict["MANAGEMENT_IP"],"PortalConnect",X)
			cnt = 1
			while True:
				cmd = "ipfs swarm peers"
				output = subprocess.check_output(cmd, shell=True)
				if "/ip4/" in output:
					print "Success to connect with IPDC peers!"
					break
				else:
					print "Connecting to IPDC peers...("+str(cnt)+")"
					cnt += 1
					time.sleep(1)
					if cnt > 10:
						print "Please check if Portal IP is correct in ipdc.conf.\n"
						print "Starting IPDC failed, please stop it first.\n"
						break
	except:
		print "Oops! There are some problems on your device so that you can't connect to Portal...\n"
