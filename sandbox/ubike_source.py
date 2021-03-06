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

from chainsrc.ubike import UbikeSource

begin = time.time()

# 顯示
s = UbikeSource()

for item in s.getPoints():
	if u'港墘' in item['name']:
		print(json.dumps(item, indent=3, ensure_ascii=False))
		print('%s %s (%s,%s)' % (item['ref'], item['name'], item ['lat'], item['lon']))

print(s.summary())

elapsed = time.time() - begin
print('取得 U-bike 站點資訊共花費 %.2f 秒' % elapsed)
