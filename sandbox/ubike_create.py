# coding: utf-8
#
# OSM 資料更新實驗程式
#
# http://wiki.openstreetmap.org/wiki/Osmapi
# http://wiki.openstreetmap.org/wiki/API_v0.6
# http://osmapi.divshot.io/
#
# 測試圖資
# 0122 捷運港墘站(2號出口) (25.079681,121.575458)
#

import os
from osmapi import OsmApi

# 注意!! 實驗階段指向測試伺服器
host = 'api06.dev.openstreetmap.org'
user = 'virus.warnning@gmail.com'
pwf  = '%s/.osmpass' % os.environ['HOME']

# 注意!! 有中文的地方需要使用 unicode 字串型態
chset = {
	u'comment':    u'自動同步 U-bike 租借站',
	u'created_by': u'小璋流同步機器人 (osmapi/0.6.0)'
}

node = {
	u'lat': 25.079681,
	u'lon': 121.575458,
	u'tag': {
		u'name':     u'捷運港墘站(2號出口)',
		u'ref':      u'0122',
		u'amenity':  u'bicycle_rental',
		u'brand':    u'微笑單車',
		u'operator': u'巨大機械工業股份有限公司'
	}
}

api = OsmApi(api=host, username=user, passwordfile=pwf)
api.ChangesetCreate(chset)
n = api.NodeCreate(node)
cid = api.ChangesetClose()

# 更新結果摘要
print('Changeset 編號: %d' % cid)
print('URL: http://api06.dev.openstreetmap.org/changeset/%d' % cid)
print('Node 編號: %s' % n['id'])
print('URL: http://api06.dev.openstreetmap.org/api/0.6/node/%s' % n['id'])
