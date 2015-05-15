# integrality_check
檢查圖資完整性，使用 Python 單元測試架構

單元測試報告，可以到這裡觀察每日執行結果

http://tacosync.com/osm/report.html

### 用法
```sh
cd ~/pv2/integrality_check
../bin/python runtest.py > report.html
```

### 建議環境
* virtualenv 安裝於 ~/pv2
* repo 位於 ~/pv2/integrality_check

### 相依套件
#### Ubuntu 14.04 LTS
```sh
sudo apt-get install postgresql-server-dev-9.3
cd ~/pv2
bin/pip install psycopg2
```
