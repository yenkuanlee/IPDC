# IPDC
IPDC(InterPlanetary Distributed Computing) is the Distributed Computation service, A peer-to-peer hypermedia protocol to make the computation faster, open, and more scalable.

## 簡介

IPDC 一個建構在 IPFS 上的分散式運算系統 (或服務)。

傳統的 [IPFS](https://ipfs.io/) 是一個星際式分散式檔案系統, 使用者可以方便快速的將自己的電腦加入 IPFS 星際, 加入後便可將自己的檔案(或目錄)進行上傳, 下載, 同步...等動作。

IPFS 目前積極與 Blockchain 整合, 目標是成為區塊鏈底層的儲存空間 (兩者底層資料結構皆為 Merkle Dag, 不論結構與用途皆具高度相容性)。

即使 IPFS 目前看來具有高度前瞻性, 似乎大部分的人的觀點還是單純在[儲存](#storage)的面相(儲存速度, 備份, 資料安全等)。 然而, 當大量使用者加入 IPFS 貢獻出儲存空間時, 這些設備的運算資源也是非常珍貴的！ IPDC 希望可以充分利用這些運算資源。

IPDC 建構在 IPFS 上, 透過 MQTT 技術實現 M2M 的溝通, 目前使用 Map-Reduce 的架構, 實作出一個 Multi-Master 的極輕便分散式運算系統。使用者加入 IPFS 後,在自己的設備上 clone 此專案, 便可以在專案底下的 Map.py 與 Reduce.py 中撰寫邏輯。簡單設定後(分散數與讀檔路徑等)便可觸發運算。 此時 IPFS 中的所有 peers 都是 IPDC 的 compute node, 運算結束後會將結果寫到觸發的設備上。

關鍵字
  - 大數據分析
  - 邊緣運算
  - AI

## 使用方法
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
