import os
IpList = ['192.168.122.39','192.168.122.40','192.168.122.71','192.168.122.171']
for x in IpList:
	os.system("scp Dmqtt.py "+x+":/tmp")
