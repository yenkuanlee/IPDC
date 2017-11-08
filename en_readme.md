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

```
$ python deploy.py init
```

Install some tools :
- IPFS
- MQTT (paho, mosquitto)
- Tensorflow (CPU version)
- Ethereum (geth, web3)


### 4. IPDC start

```
$ python deploy start
```

Start IPFS daemon and MQTT listener to become a IPDC node.




## Starting IPDC project

### IPDC MR

### IPDC TF

### IPDC CL

### IPDC ER

### IPDC EM
