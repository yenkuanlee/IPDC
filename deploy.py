import os
import sys
from subprocess import Popen

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
            p = Popen(cmd.split())
            os.system("echo "+str(p.pid)+" > .ipfs/ipfs.pid")
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
            os.system("echo "+str(p.pid)+" > .ipfs/dmqtt.pid")
        except Exception as e:
            print "CREATE WORKER ERROR"

# read config
f = open('ipdc.conf','r')
Cdict = dict()
while True:
	line = f.readline()
	if not line:
		break
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

if sys.argv[1] == "stop":
	KillProcess("ipfs")
	KillProcess("dmqtt")
	os.system("rm .ipfs/*.pid")

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
	IpfsDaemon()

	# start dmqtt
	KillProcess("dmqtt")
	DmqttDaemon(Cdict["PROJECT"])
