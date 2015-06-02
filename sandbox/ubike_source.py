# coding: utf-8
#
# 天龍國 U-bike 站點資料取得程式
#
# @author 小璋丸 
#

import os
import json
import urllib
import time

begin = time.time()

# 溫柔砍站指令 (重要資訊在網頁的 196 行)
url = 'http://taipei.youbike.com.tw/cht/f12.php?loc=taipei'
cmd = 'wget \'%s\' -q -O - | head -n 196 | tail -n 1 | grep  -o "\'.*\'"' % url

# 資料結構化
# trim > url decode > json decode
p = os.popen(cmd,'r',8192)
c = p.read().strip('\'\n')
p.close()
c = urllib.unquote(c)
c = json.loads(c)

# 顯示
for key, item in c.items():
	print('%s %s (%s,%s)' % (key, item ['sna'], item ['lat'], item['lng']))

elapsed = time.time() - begin
print('取得 U-bike 站點資訊共花費 %.2f 秒' % elapsed)
