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

# 比較
s = UbikeSource()
print(s.summary())

# 同步
cid = s.sync()
print('Changeset 編號: %d' % cid)
print('URL: http://api06.dev.openstreetmap.org/changeset/%d' % cid)

elapsed = time.time() - begin
print(u'同步 (%s) 共花費 %.2f 秒' % (s.source_name, elapsed))

