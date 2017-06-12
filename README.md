# IPDC
[![](http://gateway.ipfs.io/ipfs/QmfQJez3vA7mPWRioangGM4cwsQtEvGhuZrYxq57dLJhxM)](http://ipn.io)

這是一個 Map-Reduce 分散式運算架構

請先架好 IPFS 和 python paho

並在 Map.py 與 Reduce.py 中加入運算邏輯 (目前為 WordCount 範例)

data.dat 為運算資料

執行 python test.py (裡面可以選擇分散數)

便會在 /tmp 中產生運算結果


# 原理
Controller 會將 data.dat, Map.py, Reduce.py 上傳至 IPFS

並選擇 K 台 Workers

被選中的 Worker 會使用 IPFS 下載程式與資料

用 Map-Reduce 運算變將 Key-Value 傳到對應的 Worker

最後所有結果匯集到觸發 Controller 的那台

# 系統優點
還在想
