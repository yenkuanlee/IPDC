import control
import os
import sys
a = control.Control()

# first step
if sys.argv[1] == "SetClusterSpec" or sys.argv[1]=="0":
	a.SetClusterSpec()

# second step
elif sys.argv[1] == "ClusterTrigger" or sys.argv[1]=="1":
	a.DataUpload()
	a.CallDownload()

# third step
elif sys.argv[1] == "CloseCluster" or sys.argv[1]=="2":
	a.CloseCluster()
	os.system("rm ClusterSpec.json create_worker.py")
