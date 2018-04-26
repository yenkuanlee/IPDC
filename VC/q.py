import os
import subprocess
from subprocess import Popen
import threading
import time

def VoltDBDaemon():
	os.system("rm -rf volt*")
	os.system("/home/localadmin/voltdb/bin/voltdb init")
        cmd = "/home/localadmin/voltdb/bin/voltdb start --http=localhost:8087"
        try:
            p = Popen(cmd.split(),stdout=subprocess.PIPE)
            time.sleep(2)
            fw = open('voltdb.pid','w')
            fw.write(str(p.pid))
            fw.close()
            while True:
                line = p.stdout.readline().replace("\n","")
                if "Server completed initialization" in line:
                        #print "IPDC is ready!\n"
                        break
        except Exception as e:
            print "CREATE WORKER ERROR"
            print e

def IpfsDaemon():
        cmd = "ipfs daemon"
        try:
            p = Popen(cmd.split(),stdout=subprocess.PIPE)
            time.sleep(2)
            #os.system("echo "+str(p.pid)+" > .ipfs/ipfs.pid")
            fw = open('ipfs.pid','w')
            fw.write(str(p.pid))
            fw.close()
            while True:
                line = p.stdout.readline().replace("\n","")
                if "Daemon is ready" == line:
                        print "IPDC is ready!\n"
                        break
        except Exception as e:
            print "CREATE WORKER ERROR"
            print e

def KillProcess(process):
        try:
                f = open(process+'.pid','r')
                while True:
                        line = f.readline()
                        if not line:
                                break
                        line = line.replace("\n","")
                        os.system("kill -9 "+line)
                        os.system("echo '' > "+process+".pid")
        except Exception as e:
                print e

#Vthread = threading.Thread(target=VoltDBDaemon, name='T1')
#Vthread.start()
KillProcess("voltdb")
