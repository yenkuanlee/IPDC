import control
import os
import sys
a = control.Control()
VDBHOST = "none"
VDBPORT = "8087"
f = open("/home/localadmin/IPDC/ipdc.conf",'r')
while True:
	line = f.readline()
	if not line:
		break
	line = line.replace("\n","")
	line = line.replace(" ","")
	tmp = line.split("=")
	if tmp[0] == "DATA_NODE_IP":
		VDBHOST = tmp[1].split("#")[0]
		break
if sys.argv[1] == "start":
	K = sys.argv[2]
	a.SetKRunner(int(K))
	print VDBHOST,VDBPORT,K
	a.VoltDBDaemon(VDBHOST,VDBPORT,K)
elif sys.argv[1] == "stop":
	a.CloseCluster()
	os.system("rm -rf voltdbroot")
	os.system("rm -rf *.pyc")
