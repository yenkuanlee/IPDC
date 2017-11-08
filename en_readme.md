# IPDC

IPDC(InterPlanetary Distributed Computing) is the Distributed Computation service, A peer-to-peer hypermedia protocol to make the computation faster, flexible, and more scalable.




## Abstract

IPDC is a decentralized computing system (or service) built on IPFS.

The traditional [IPFS](https://ipfs.io/) is an InterPlanetary distributed file system, users can quickly and easily add their own computers to IPFS environment. After joining IPDC, people can upload their own files (or directory), download, sync ... and so on.
IPFS is actively integrating with [Ethereum](https://ethereum.org/) with the goal of becoming the storage of the blockchain (Both the core data structure is Merkle Dag).

Even though IPFS looks highly forward-looking, it seems that most people's point of view are purely in terms of storage. However, when a large number of users join the IPFS to contribute storage space, the computing resources of these devices are also very valuable. IPDC hopes to make full use of these computing resources.

IPDC is built on IPFS and communicates with M2M through MQTT technology. IPDC is divided into five kinds of architecture currently :
- MR (Map-Reduce)
- TF (Tensorflow)
- CL (Big Crawler)
- ER (Ethereum)
- EM (Edge Computing)




## Installation Dependencies (External IP)

IPDC is built on top of IPFS, IPFS generates a ID when it is initialized (the format such as: QmNXM4uWnd7oLqqDFg4Jo26eSYWQvZz6QCmiqtzmFgJhDD).

Native IPFS initialization will connect the officially recognized gateway. The system will find the peer through the gateway and connect with other people's IPFS through ID and IP (no matter internal IP or external IP).
However, the IPFS used by IPDC is a closed IPFS that I modified the source code, the main purpose is not to let strangers connected to our IPFS cluster.
We will not connect to the IPFS official gateway, so we need external IP to connect the two nodes.

In addition, the MQTT communication mechanism that we use now also uses external fixed IP. Making IP more flexible is one of the topics that IPDC can optimize in the future.




## Getting Started


### 1. Clone the IPDC project

```
$ git clone https://github.com/yenkuanlee/IPDC
```

### 2. Set up ipdc.conf

```
$ cd IPDC
$ vi ipdc.conf
	# DOMAIN_NAME : You can only connect to peers with same domain_name
	# MANAGEMENT_IP : portal IP
	# PROJECT : MR / TF / CL / ER / EM
```

### 3. IPDC initialization

Install some tools :
- IPFS
- MQTT (paho, mosquitto)
- Tensorflow (CPU version)
- Ethereum (geth, web3)

```
$ python deploy.py init
```


### 4. IPDC start

Start IPFS daemon and MQTT listener to become a IPDC node. 


```
$ python deploy start
```




## Starting IPDC project

In this section, we will introduce how to use each of IPDC project.
All IPDC project have two python codes :
- control.py : project controller
- Dmqtt.py : mqtt listener, receive messages and do the correspond things.

Note that different IPDC projects have different logic of controll.py and Dmqtt.py.


### IPDC MR

- IPDC MR is based on Map-Reduce framework with characteristic of decentralized, multi-master and extremely light. Users can write logic in Map.py and Reduce.py under the project. All peers in IPFS can be compute nodes for IPDC (we can set the distributed number).
- There are some core code in ER project :
	- data.dat : input dataset of Mapper
	- Map.py : Mapper
	- Reduce.py : Reducer
	- test.py : Run the MR job

- The example algorithm of this project is "WordCount".

#### Running IPDC MR project
- Parameter setting
```
$ vi test.py
	# we can set the distributed number in function "SetKRunner"
```
- Input data
	- default named "data.dat". 
	- We can rename the input data name and modify some part of codes :
```
control.py:		cmd = "timeout 10 ipfs add data.dat"
Dmqtt.py:		os.system("rm Map.py* Reduce.py* output.txt data.dat")
Map.py:		self.InputPath = 'data.dat'
```
- Mapper
	- The bottom of function "RunMap" in Map.py can write some mapper logic.
- Reducer
	- Function "reduce" in Reduce.py can write some reducer logic.
- Run the MR job
```
$ python test.py
```
- Output
	- JobID represent the timestamp of running MR job.
	- The result of the execution is written to /tmp/JobID .
	- There are K results with K distributed number.
```
$ cat /tmp/JobID/*
```

#### Theorem of IPDC MR
- The controller determines and chooses K (distributed number) workers through the peerID hash of each node in IPDC.
- The controller will upload the input file, Map.py, Reduce.py to IPFS and notify K workers through MQTT to download the file.
- The controller call each workers by MQTTto start the Mapper. By using worker's peerID and line number of input file as key, we can assign a worker several keys to map.
- As with Hadoop, mapper eventually throws the result as Key-Value pair into the corresponding buffer.
- Each worker's Buffer finish to collect Key-Value pair and starting reduce job .
- After the end of each reducer, the results will be written into local disk and upload to IPFS. Through the MQTT, output hash will be passed to master who triggered the MR job.
- MR master collected and download all output hash of each workers,and finish the entire MR job.


### IPDC TF
- IPDC node can establish tensorflow cluster
	- https://learningtensorflow.com/lesson11/
- IPDC TF is the framework of distributed tensorflow. Users fill in the virtual cluster specification file (ClusterSpec.conf). Then IPDC picks compute nodes from IPFS peers and produces real cluster specs (ClusterSpec.json) to upload to IPFS, so the controller can notify all compute nodes through MQTT to complete the establishment of distributed tensorflow cluster.



#### Running IPDC TF project
- Set ClusterSpec
- Generate create_worker.py
- Cluster deploy
- User coding
- Execution


### IPDC CL


### IPDC ER


### IPDC EM
