# 區塊鏈交易雛型應用於台灣農產品批發交易市場
## Apply the trading prototype in blockchain to agricultural commodities of the wholesale market in Taiwan

### 1.簡介 (Introduction)
 現行台灣農產品批發市場使用拍賣方式交易進行，尚未使用電子交易模式進行交易，故使用此交易雛形證明其安全性與可行性。
 The current trading model of the wholesale market of agricultural commodity in Taiwan conducts manual auctions, and it hasn't adopted electronic trading yet. So, we created this prototype to prove its safety and feasibility. 

### 2.使用工具 (Tools)
- Python for data processing and function execution 
- ArrangoDB for data storage

### 3.流程 (Process)   
a.  模擬交易雛型 (Simulated Trading Prototype)  
* 00-Suppliers-Buyers: 暫由隨機產生資料 (Using faker to generate buyer's and supplier's information) 
* 01-Products: 匯入商品資料 (Importing information of price and name of agricultural commodity)
* 02-SupplierOffers: 模擬賣家可提供商品 (Simulated to generate the market list from the supplier)
* 03-SupplierOffers: 買家查找可提供指定商品之賣家 (Establishing a search function for buyer)
* 04-MarketTrade: 某交易日中買賣搓合商品交易 (Simulating a condition of daily trade)
* 07-BlockChainTrade: 鎖存某交易日中買賣搓合商品交易 (lock down the trading data as a daily blockchain)

b. 驗證功能 (The Function of Validation)
* 05-MarketTrade & 06-MarketTrade: 買賣家交易統計 (Trading statistics of buyer and supplier)
* 08-BlockChainTrade: 商品交易區塊驗證 (Verification of blockchain information)

### 4.資料 (Data) -- csv 檔 (file) 
* 供應商 (Suppliers)
* 買家 (Buyers)
* 商品與價格 (Commodity & Price)
* 每日市場供應 (Daily Supplement)
* 每日商品交易 (Daily Trade)
* 區塊鏈交易金鑰 (Track Key of blockchain)

### 5.備註 (Remark)
* 商品資料需額外處理與準備 (The data of commodity should be processed and prepared additionally)
* 細節可參考該論文 (detailed explanation refer to https://hdl.handle.net/11296/6jr667)
