# IPDC
IPDC(InterPlanetary Distributed Computing) is the Distributed Computation service, A peer-to-peer hypermedia protocol to make the computation faster, open, and more scalable.

## Abstract

IPDC 一個建構在 IPFS 上的分散式運算系統 (或服務)。

傳統的 [IPFS](https://ipfs.io/) 是一個星際式分散式檔案系統, 使用者可以方便快速的將自己的電腦加入 IPFS 星際, 加入後便可將自己的檔案(或目錄)進行上傳, 下載, 同步...等動作。

IPFS 目前積極與 Blockchain 整合, 目標是成為區塊鏈底層的儲存空間 (兩者底層資料結構皆為 Merkle Dag, 不論結構與用途皆具高度相容性)。

即使 IPFS 目前看來具有高度前瞻性, 似乎大部分的人的觀點還是單純在[儲存](#storage)的面相(儲存速度, 備份, 資料安全等)。 然而, 當大量使用者加入 IPFS 貢獻出儲存空間時, 這些設備的運算資源也是非常珍貴的！ IPDC 希望可以充分利用這些運算資源。

IPDC 建構在 IPFS 上, 透過 MQTT 技術實現 M2M 的溝通, 目前分成 MR 與 TF 兩種架構。

IPDC MR 是建立在 Map-Reduce 的架構, 實作出一個 Multi-Master 的極輕便分散式運算系統。使用者加入 IPFS 後,在自己的設備上 clone 此專案, 便可以在專案底下的 Map.py 與 Reduce.py 中撰寫邏輯。簡單設定後(分散數與讀檔路徑等)便可觸發分散式運算。 此時 IPFS 中的所有 peers 都是 IPDC 的 compute node, 運算結束後會將結果寫到觸發的設備上。

IPDC TF 為 distributed tensorflow 的架構，使用者加入 IPFS 後,在自己的設備上 clone 此專案, 並填寫虛擬的 cluster 規格設定(ClusterSpec.conf), 則 IPDC 會從 peers 中挑選 compute nodes, 並產生真正的 cluster 規格(ClusterSpec.json) 上傳到 IPFS, 透過 MQTT 通知所有 compute node 完成建立 distributed tensorflow cluster。使用者可以參考 cluster 規格撰寫並執行分散式 tensorflow 程式。

關鍵字 :
- 大數據分析
- 邊緣運算
- Deep Learning
- Big Crawler

## Install Dependencies
### 1. 可對外固定 IP
IPDC 建構在 IPFS 之上, IPFS 在安裝時會產生一組ID (格式如 : QmNXM4uWnd7oLqqDFg4Jo26eSYWQvZz6QCmiqtzmFgJhDD)。

原生的 IPFS 初始化會連接官方認可的 gateway, 所以就算 IP 不對外甚至內網(192.168.x.x), 都可以跟其他人的 IPFS 連接 (系統會透過 gateway 搜尋 ID 找到 peer 並串連)。

然而 IPDC 使用的 IPFS 是我修改過原始碼的封閉型 IPFS, 主要目的是不讓陌生人連到我們的 cluster。 因此我們不會連到 IPFS 官方 gateway, 所以需要可對外的 IP 才能讓兩個 node 相連。

除此之外, 我們使用的 MQTT 溝通機制目前亦使用可對外固定 IP。 讓 IP 更有彈性是 IPDC 未來可優化的議題之一。

### 2. 安裝封閉式 IPFS (現在有 deploy.py，不用這步驟啦嘿嘿)
下載封閉式 IPFS 執行檔

```
  $ wget https://gateway.ipfs.io/ipfs/QmeNGsAMcnnkydGpze5x5K5cwf451T6BdJmr1QzPFqkwtD
  $ mv QmeNGsAMcnnkydGpze5x5K5cwf451T6BdJmr1QzPFqkwtD ipfs
  $ sudo chmod 777 ipfs
  $ sudo mv ipfs /usr/local/bin
  $ ipfs
```
  
產生設定檔

- 封閉式 IPFS 是之前為了 iServStor 產品設計的, 所以設定檔是 iservstor.conf, 就先姑且用吧...
  
```
  $ sudo mkdir -p /opt/iservstor/conf
  $ sudo vi /opt/iservstor/conf/iservstor.conf
    DOMAIN_NAME = IPDC
    # 加入以上 Domain Name 資訊, 相同 Domain Name 的 peer 才能相連 ！
```
  
初始化

```
  $ ipfs init
```

啟動 IPFS daemon

```
  $ ipfs daemon
```


### 3. 安裝設定 MQTT (現在包含在 deploy.py init 中，不用這步驟啦嘿嘿)

安裝 mosquitto

```
  $ sudo apt-get install mosquitto mosquitto-clients
  $ sudo service mosquitto start
```

安裝 paho
```
  $ pip install paho-mqtt
```

## Getting Started

加入 IPDC (20170906)

```
  $ git clone https://github.com/yenkuanlee/IPDC
  $ cd IPDC
  * 更改設定檔 ipdc.conf
  $ python deploy.py init    # 初始化, 安裝 MQTT 與 tensorflow python 2.7 cpu version
  $ python deploy.py start    # start IPDC
  * 開始使用 IPDC / 被使用 IPDC
  $ python deploy.py stop    # close IPDC
  
```

加入 IPDC (Old)

```
  $ git clone https://github.com/yenkuanlee/IPDC
  $ cp Dmqtt.py /tmp
  $ python /tmp/Dmqtt.py &      # 背景執行 Dmqtt, 成為 IPDC Data Node 一員
```

設定 IPDC MR

- IPDC 現有架構為 Map-Reduce 架構, 可以設定分散數與 input 檔路徑
- test.py 中可以設定分散數
- Map.py 中可以設定 input 檔路徑

IPDC Map-Reduce 邏輯撰寫

- Map.py 中的 RunMap 的最下方可以寫入 Map 邏輯
- Reduce.py 中的 reduce 中可以寫入 reduce 邏輯
- 本專案的 Map-Reduce 演算法為 WordCount

IPDC MR 執行分散式運算

```
  $ python test.py
```

- JobID 為執行當下的 timestamp
- 執行結果寫入 /tmp/JobID
- 分散數為 K 則會有 K 份結果
- 印出結果

```
  $ cat /tmp/JobID/*
```


## IPDC MR 原理

1. Controller 透過 IPDC 中各個 node 的 peerID hash 來判斷並選擇 K(分散數) 個 workers
2. Controller 會將 input 檔, Map.py, Reduce.py 上傳至 IPFS, 並透過 MQTT 通知 K 個 workers 將檔案下載
3. Controller 透過 MQTT 呼叫各個 worker 開始 Map 的工作, 透過 worker peerID 加上 input 檔行數為 key, 可以分配個台 worker 該負責哪些 key
4. 如同 Hadoop 一般, Map 最後會將結果以 Key-Value 形式丟給對應的 Buffer
5. 各台 worker 的 Buffer 蒐集完 Key-Value 後開始進行 Reduce
6. 各台結束 Reduce 後, 將結果寫入 Local 便上傳至 IPFS, 再透過 MQTT 將 output hash 傳給觸發 MR 的 master
7. Master 蒐集完所有 worker 的 output hash, 將這些 hash 下載, 結束整個 MR job


## IPDC MR 之 MQTT channel

* IPDC 是一個極具彈性的框架，而 IPDC MR 是在此框架下實作出一個分散式運算的 Map-Reduce 架構
* Dmqtt.py 是 IPDC 的核心，透過 channel 的制定可以實現各種分散式運算架構
* IPDC MR 的 Dmqtt.py channel 包含 
  * Download : 通知 worker 下載檔案
  * DoMap : 通知 worker 進行 Map
  * Buffer : 將 Map 產生的 Key-Value 傳給對應的 worker
  * GetResult : 各台 worker Reduce 結果傳給 Master 
  * CleanUp : 各台 worker 刪除不必要的檔案


## IPDC TF

- IPDC TF 需要先安裝 tensorflow (python 2.7 / CPU 版本)
    - 執行 python deploy.py init 即可安裝完成

- IPDC 的 node 可以建立 tensorflow 的 cluster
    - https://learningtensorflow.com/lesson11/ 


1. set ClusterSpec
	- json 虛擬規格
		- task name
		- task ip/port list 不需要給 !!!! ( IPDC 自動依照 worker 數配置 )
		- task index
	- ex : {"local": [0, 1]}
		- task name : local
		- task index 分別是 0, 1
		- worker 數是 2
2. 產生 create_worker.py
	- IPDC 配置 worker, 生成真正的 ClusterSpec json
		- cluster = tf.train.ClusterSpec({"local": ["192.168.122.171:2222", "192.168.122.40:2222"]})
			- IP 從 ipfs swarm peers 算最短距離 n 個 hash 取得
			- port 暫定 2222
	- 專案底下生成 ClusterSpec.json
		- {"TaskIndex": {"192.168.122.171:2222": 0, "192.168.122.40:2222": 1}, "ClusterSpec": {"local": ["192.168.122.171:2222", "192.168.122.40:2222"]}} 	＃( 加入 task index 資訊 )
	- User 可以針對產生的 create_worker.py 進行修改

3. Cluster deploy
	- 上傳 create_worker.py 與 ClusterSpec.json to IPFS
	- message queue to workers
	- worker 的 Dmqtt 接收到 message
		- 下載 create_worker.py 與 ClusterSpec.json
		- 配置 task index 並啟動 create_worker.py
4. User coding
	- 參考 ClusterSpec.json 資訊撰寫程式
		- example.py 為範例程式
	- 執行分散式 tensorflow

5. 實際執行方式
	- python test.py 0
		- 產生 create_worker.py 與 ClusterSpec.json
	- python test.py 1
		- 設定並啟動 IPDC tensorflow cluster
	- python example.py
		- 執行分散式 TF
	- python test.py 2
		- 關閉所有 worker, 並刪除 create_worker.py 與 ClusterSpec.json

## IPDC 優勢

* 極度輕便
  * IPDC 框架僅 400 行程式，安裝簡單 
  * IPFS 與 MQTT 亦可在各種設備上安裝 
  * 即使是記憶體容量只有128MB大小的 Raspberry Pi 單板電腦也能用 
* 極具彈性 
  * IPDC 是一個極具彈性的框架，透過制定 Dmqtt.py 的 channel 並修改 control.py 的邏輯以及增加必要程式，便可實現各種分散式架構 
  * 不受限於特定分散式架構 
  * 使用者可以有彈性的 加入 / 退出 IPDC (針對此項目, IPDC 目前還不能做到, 但確定可行)
* Scalable 
  * IPFS 可跨網域增長 
  * 願意加入 IPDC 的使用者, 可簡單快速的納入這個巨大的 cluster 
* 開放且快速 
  * IPDC 承襲 IPFS 的優點，讓資料與程式存在 IPFS 中 
    * Hash 透過 MQTT 傳遞, 讓資料與程式更開放 
    * IPFS 的 Merkle Dag 結構讓資料 Deduplicate, 節省儲存空間 
    * IPFS 下載資料與程式時, 會再 Merkle Dag 走訪並平行去各台 peer 抓取需要的檔案碎片, 提升取得檔案之速度 
    * 可透過 IPFS 強化資料的備份
  * IPDC 也有 MQTT 的優點 
    * 快速傳遞訊息的 protocal 
    * M2M 符合 IPFS 去中心化的優點, 增加運算效率 
    * 將 IPFS 從儲存提升到運算的境界 
* Multi-Master 架構
  * IPDC 的任一個 node 皆可以是 master, 也能成為別人的 worker 
  * 解決 Master-Slaves 負載不平衡, 資源不對等的問題 
  * 優於現有的邊緣運算架構, 所有的 node 都有控制機制, 更能提升運算效率 
  * 完全去中心化, 將不必要的傳輸降到最低 


## IPDC 發展方向

如前述所言，IPDC 是一個極具彈性的框架，透過制定 Dmqtt.py 的 channel 並修改 control.py 的邏輯以及增加必要程式，便可實現各種分散式架構。 以下是目前想到 IPDC 的應用情境與發展方向，使用者的 node 可以成為 :

* MR 的 Mapper / Reducer 
  - IPDC MR


* Deep Learning 的神經元 
  - IPDC TF


* 邊緣運算的 edge


* Big Crawler 的種子 


* 區塊鏈的礦工

## Reference

- 新聞
  - [邊緣運算關鍵技術AI，讓瑞典工具機大廠異常預警速度加快20倍](http://www.ithome.com.tw/news/114626)
  - [The next multibillion-dollar tech market was quietly born this year, says A-list VC Peter Levine](http://www.businessinsider.com/edge-computing-is-the-next-multi-billion-tech-market-2016-12)
  - [Edge Analytics Market worth 7.96 Billion USD by 2021](http://www.marketsandmarkets.com/PressReleases/edge-analytics.asp)
- 論文 
  - [Edge-centric Computing: Vision and Challenges](http://dl.acm.org/citation.cfm?doid=2831347.2831354)
  - [Nebula: Distributed Edge Cloud for Data Intensive Computing](http://www-users.cselabs.umn.edu/classes/Spring-2017/csci8980/papers/GeoEdge/nebula.pdf)
  - [Cost-Effective Content Delivery Networks Using Clouds and Nano Data Centers](https://link.springer.com/chapter/10.1007/978-3-642-41671-2_53)
- 其他 (了解中)
  - [Dapp](https://medium.com/@FEhrsam/the-dapp-developer-stack-the-blockchain-industry-barometer-8d55ec1c7d4)
