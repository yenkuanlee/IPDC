# IPDC

IPDC(InterPlanetary Distributed Computing) is the Distributed Computation service, A peer-to-peer hypermedia protocol to make the computation faster, flexible, and more scalable.




## Table of Contents
- [Abstract](#abstract)
- [Installation Dependencies](#installation-dependencies)
	- [External IP](#external-ip)
- [Getting Started](#getting-started)
	- [1. Clone the IPDC project](#1.-clone-the-ipdc-project)
- [Starting IPDC project](#starting-ipdc-project)
- [Advantage of IPDC](#advantage-of-ipdc)
- [License](#license)




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




## Installation Dependencies 

### External IP

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
- There are some core code in TF project :
	- ClusterSpec.conf : virtual cluster specification file
	- example?.py : example code
	- test.py : Run the TF job



#### Running IPDC TF project
- Set ClusterSpec
	- virtual specs in json
		- task name
		- task index
	- ex : {"local": [0, 1]}
		- task name : local
		- task index is 0, 1 respectively
		- number of workers is 2
- Generate create_worker.py
	- IPDC picks worker, and generate a real ClusterSpec in json.
		- cluster = tf.train.ClusterSpec({"local": ["192.168.122.171:2222", "192.168.122.40:2222"]})
			- IP is picked from IPFS peers by nn.
			- Setting port to 2222 for now.
	- Generate ClusterSpec.json under the project.
		- {"TaskIndex": {"192.168.122.171:2222": 0, "192.168.122.40:2222": 1}, "ClusterSpec": {"local": ["192.168.122.171:2222", "192.168.122.40:2222"]}}
		- User can modify the generated create_worker.py.
- Cluster deploy
	- Upload create_worker.py and ClusterSpec.json to IPFS.
	- message queue to workers.
	- Dmqtt of worker received the message.
		- Download create_worker.py and ClusterSpec.json.
		- Configure the task index and run create_worker.py.
- User coding
	- Coding in accordance with ClusterSpec.json.
		- there are there sample code in the TF project.
	- run the distributed tensorflow job
- Execution
```
$ python test.py 0
	# generate create_worker.py and ClusterSpec.json
$ python test.py 1
	# Set and start IPDC tensorflow cluster
$ python example.py
	# run the distributed tensorflow job
$ python test.py 2
	# Close all workers and delete create_worker.py and ClusterSpec.json
```


### IPDC CL
- IPDC CL is a simple distributed framework. Each compute node will do a indepentdant operation.
- The idea comes from TAAI 2015's paper
	- https://drive.google.com/file/d/0B_NX2TXJp4ItVlV0Z1ZfZkVoYzA/view?usp=sharing
	- Through the Apache Pig's UDF, let each node in the Cluster operate independently, and then complete the results.
- In this project, we use a crawler to be a CL example, which can be distributed by target url and crawl independently.
- There are some core code in CL project :
	- GetData.py : get some data to crawl
	- data.dat : dataset from GetData.py
	- crawler.py : crawler (suitable for any independently distributed job)
	- test.py : Run the CL job

#### Running IPDC CL project
```
$ python GetData.py > data.dat
$ vi test.py
	# we can set the distributed number in function "SetKRunner"
$ python test.py 
	# Run the CL job
```


### IPDC ER
- IPDC ER combines IPFS node with private ethereum node. There are several benefits :
	- Users can save files to IPFS, and put the file hash into ethereum.
	- Users can provide their devices for building some private chain.
	- Chain owner can ask resource to build a private chain through IPDC so that he can manage some blockchain application.
	- The blockchain architecture is 100% suitable for IPDC.
- There are three roles of IPDC ER users
	- Resource owner : IPDC node, people who contribute his devices to IPDC.
	- Chain owner : IPDC node, people who want to use some IPDC nodes to build his private chain for some purpose.
	- Chain user : Non IPDC node, people who just use the specific chain, and need not to know anything about IPDC.
- IPDC ER is just a blockchain platform. The important thing is that we can run many Dapps on IPDC.
	- Filesign is a wonderful example of Dapp in project ER.
- There are some core code in ER project :
	- description.conf : fill in some basic information for building a chain
	- enode_setting.py : set IPDC node to become a ethereum node
	- ObjectNode.py : control of IPFS merkle dag data structure
	- LocalVigilante.py : correct some bad things
	- chain.py : ask_resource / start / stop / add_node for one chain
	- CheckDB.py : check the situation of local database
	- CheckPeer.py : check the situation of ethereum peers

#### Running IPDC ER project
- set description.conf
	- When the chain owner want to create a chain, he needs to create a file named description.conf under IPDC ER project.
	- There are some arguments which the chain owner have to fill in :
		- chainname : name of the chain
		- networkid : only the same networkid of two IPDC ER node can be connected to one chain.
		- chaintype : type of the chain
		- description : description of the chain
		- extradata : an argument of ethereum
		- numberofnode : how mant IPDC node you want to use
		- rpcport : always 8545 in IPDC ER
		- date
	- You can refer to the following format of description.conf
	```
	networkid = 13467912
	chaintype = filesign
	description = This is a kevin chain.
	extradata = 12345
	numberofnode = 3
	rpcport = 8545
	date = 2017-11-02T11:00:00
	chainname = Kevin
	```
- ask resource
	- There are an parameter in chain.py is "AskResource"
		- if AskResource is False, IPDC will skip the step and build a chain directly.
		- if AskResource is True, IPDC will ask resource from IPDC ER node before building a chain.
	- If "AskResource" in chain.py is set to True, you should do the following command. IPDC will send your description.conf to IPFS, and publish the request by MQTT to find some ER node who want to help you to build a chain.
	```
	$ python chain.py ask_resource
	```

	- After chain owner publish his request to IPDC, each resource owner will received the message and record the chain information into a sqlite database(/tmp/.db/chain.db). If one resource owner want to join this chain, he can do the following things:
	```
	$ sqlite3 /tmp/.db/chain.db

	sqlite> select * from AskResource;
	QmRxiJ3WjG5YFQSWY3mdXAKBRgfLyyocFwL9cTBEpcfhwX|Kevin|filesign|3|13467912|12345|8545| This is a kevin chain.
		# You can see information of the chain

	# If resource owner want to join the chain, he can do the following command.
	$ IPFS pin add QmRxiJ3WjG5YFQSWY3mdXAKBRgfLyyocFwL9cTBEpcfhwX
	```
- Start a chain
	- If contributors of resource owner are enough to build a chain (refer to the value of numberofnode in description.conf), the chain owner can do the following command to start his chain :
	```
	$ python chain.py start
	```
	- Chain owner can manage some application in a chain.
		- Basic ethereum transaction.
		- Filesign will be introduced in the next section.
	- After a chain is built, chain owner can add IPDC nodes to the chain.
	```
	$ python chain.py add_node 2
		# add two nodes to the chain
	```
- Stop a chain
	- Chain owner can stop the chain
	```
	$ python chain.py stop
	```

#### Filesign : a Dapp example
- Filesign is a command line tool built on IPDC ER. It is an application about sending the certificate and verify the certificate. There are three roles in the filesign application :
	- Sender : people or organization who send the certificate to someone
	- Receiver : people who receives the certificate
	- Varifier : people who want to verify someone's certificate
- Filesign command line tool is put on every IPDC ER node, each IPDC ER node is a filesign sender. In the other words, a resource owner in one chain is also a filesign sender node. A filesign sender can create many account of filesign receivers and send certificate to them; A filesign receiver can request the sender to download his certificate which is stored in IPFS; A filesign varifier can upload someone's certificate to filesign sender node to varify the certificate.
- Execution
```
# To the path of FileSign
$ cd /path/to/ER/FileSign

# For sender
$ python filesign.py account new
	# create an receiver account
$ python filesign.py file send
	# send certificate to a receiver

# For receiver request
$ python filesign.py file download
	# download the receiver's certificate

# For varifier request
$ python filesign.py varify
	# upload certificate and varify 
```

### IPDC EM
- IPDC EM is not a clear architecture. It is an attitude !
- IPDC EM node can become a gateway of edge computing.




## Advantage of IPDC
- Extremely light
	- IPFS and MQTT can be installed on a variety of devices.
	- Even a Raspberry Pi single-board computer with a memory capacity of only 128MB can be used.
- Extremely flexible
	- IPDC is a very flexible framework that enables a wide range of decentralized architectures by making the Dmqtt.py channel and modifying the logic of control.py and adding the necessary code.
	- Not limited to a specific decentralized architecture.
	- Users can flexibly join / exit IPDC
- Scalable
	- IPFS can grow across domains
	- Users willing to join IPDC can easily and quickly incorporate the huge cluster.
- Open and fast
	- IPDC inherits the advantages of IPFS, so that data and code exist in the IPFS.
		- Hash passed through MQTT to make data and code more open
		- Merkle-Dag data structure in IPFS make data deduplicate and saving space of storage.
		- IPFS download data and code by visiting Merkle Dag, parallel to each peers to capture the required file fragments, to enhance the speed of access to files.
		- IPFS enhanced data backup.
	- IPDC also has the advantage of MQTT
		- high speed to publish message.
		- M2M conforms to the advantages of IPFS decentralization, increasing computing efficiency.
		- Enhance IPFS from storage to computing.
- Multi-Master architecture
	- Any IPDC nodes can be master, but also can be someone else's worker.
	- Solve the problem of unbalanced load of Master-Slaves.
	- Better than the existing edge computing architecture, to improve computing efficiency.
	- Completely decentralized and minimize the redundant transmission.




## License
MIT
