# 戰時網路模擬器
## Introduction
戰爭時網路長什麼樣子呢？我對於戰時網路的想像是，台灣的國內網路非常多元（固網、第四台寬頻網路、4G、5G），電力也逐漸走向分散式智慧電網，所以戰爭時發生完全斷網斷電的機會並不高，但是台灣因為是海島，連到國際網路主要靠海纜，而海纜是容易被惡意弄斷的，因此戰時只剩下衛星網路可用，但是衛星網路頻寬有限，因此可能會優先保留給政府或軍事用途，而不是給民間使用，因此可假設戰時國外服務都會中斷，包含 Line, FB, Youtube, Google, Google Map, GMail ... 。

情境：「發生戰爭時，透過 Google 搜尋『防空避難所』並透過 Google Map 顯示最近的避難所位置」
上面這個情境會因為連不到 Google 搜尋和 Google Map 而無法使用
因此我們需要盤點測試，過去我們有多少情境是用到國外的網路，我們必須要全部國內化以因應戰時準備
為了要測試，因此建立了「戰時網路模擬器」，這是個 DNS Server ，只要將自己電腦改指到這個 DNS Server ，你就只能連到國內網路
藉此可以知道還有什麼服務可以用

## 安裝
### 初始化
```
$ git clone https://github.com/g0v/wardns
$ cd worddns
$ curl https://cdn.jsdelivr.net/npm/geolite2-city@1.0.0/GeoLite2-City.mmdb.gz | gunzip > GeoLite2-City.mmdb
$ python3 -m venv venv
```

### 啟動 dns server
```
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 dnsserver.py
```

### 或使用 docker
```
$ git clone https://github.com/g0v/wardns
$ cd worddns
$ docker compose up
```

### 把自己的電腦的 DNS 改成 127.0.0.1 測試

## License
程式碼以 BSDLicense 授權
