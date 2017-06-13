# IPDC
IPDC(InterPlanetary Distributed Computing) is the Distributed Computation service, A peer-to-peer hypermedia protocol to make the computation faster, open, and more scalable.

## 簡介

IPDC 一個建構在 IPFS 上的分散式運算系統 (或服務)。

傳統的 [IPFS](https://ipfs.io/) 是一個星際式分散式檔案系統, 使用者可以方便快速的將自己的電腦加入 IPFS 星際, 加入後便可將自己的檔案(或目錄)進行上傳, 下載, 同步...等動作。

IPFS 目前積極與 Blockchain 整合, 目標是成為區塊鏈底層的儲存空間 (兩者底層資料結構皆為 Merkle Dag, 不論結構與用途皆具高度相容性)。

即使 IPFS 目前看來具有高度前瞻性, 似乎大部分的人的觀點還是單純在[儲存](#storage)的面相(儲存速度, 備份, 資料安全等)。 然而, 當大量使用者加入 IPFS 貢獻出儲存空間時, 這些設備的運算資源也是非常珍貴的！ IPDC 希望可以充分利用這些運算資源。

IPDC 建構在 IPFS 上, 透過 MQTT 技術實現 M2M 的溝通, 目前使用 Map-Reduce 的架構, 實作出一個 Multi-Master 的極輕便分散式運算系統。使用者加入 IPFS 後,在自己的設備上 clone 此專案, 便可以在專案底下的 Map.py 與 Reduce.py 中撰寫邏輯。簡單設定後(分散數與讀檔路徑等)便可觸發運算。 此時 IPFS 中的所有 peers 都是 IPDC 的 compute node, 運算結束後會將結果寫到觸發的設備上。

關鍵字 :
- 大數據分析
- 邊緣運算
- Deep Learning
- AI

## Install Dependencies
### 可對外固定 IP
IPDC 建構在 IPFS 之上, IPFS 在安裝時會產生一組ID (格式如 : QmNXM4uWnd7oLqqDFg4Jo26eSYWQvZz6QCmiqtzmFgJhDD)。

原生的 IPFS 初始化會連接官方認可的 gateway, 所以就算 IP 不對外甚至內網(192.168.x.x), 都可以跟其他人的 IPFS 連接 (系統會透過 gateway 搜尋 ID 找到 peer 並串連)。

然而 IPDC 使用的 IPFS 是我修改過原始碼的封閉型 IPFS, 主要目的是不讓陌生人連到我們的 cluster。 因此我們不會連到 IPFS 官方 gateway, 所以需要可對外的 IP 才能讓兩個 node 相連。

除此之外, 我們使用的 MQTT 溝通機制目前亦使用可對外固定 IP。 讓 IP 更有彈性是 IPDC 未來可優化的議題之一。

### 安裝封閉式 IPFS
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
    DOMAIN_NAME = kevin
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

請先架好 IPFS 和 python paho


## Nothing
[![](http://gateway.ipfs.io/ipfs/QmfQJez3vA7mPWRioangGM4cwsQtEvGhuZrYxq57dLJhxM)](http://ipn.io)

- [星際分散式運算](#IPDC)

這是一個 Map-Reduce 分散式運算架構

請先架好 IPFS 和 python paho

並在 Map.py 與 Reduce.py 中加入運算邏輯 (目前為 WordCount 範例)

data.dat 為運算資料

執行 python test.py (裡面可以選擇分散數)

便會在 /tmp 中產生運算結果


## 原理
Controller 會將 data.dat, Map.py, Reduce.py 上傳至 IPFS

並選擇 K 台 Workers

被選中的 Worker 會使用 IPFS 下載程式與資料

用 Map-Reduce 運算變將 Key-Value 傳到對應的 Worker

最後所有結果匯集到觸發 Controller 的那台

## 系統優點
還在想
