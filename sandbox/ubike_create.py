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
node = {
	'lat': 25.079681,
	'lon': 121.575458,
	'tag': {
		'name':     u'捷運港墘站(2號出口)',
		'ref':      '0122',
		'amenity':  'bicycle_rental',
		'brand':    u'微笑單車',
		'operator': u'巨大機械工業股份有限公司'
	}
}

api = OsmApi(api=host, username=user, passwordfile=pwf)
api.ChangesetCreate()
n = api.NodeCreate(node)
api.ChangesetClose()

print('Node 編號: %s' % n['id'])
print('URL: http://api06.dev.openstreetmap.org/api/0.6/node/%s' % n['id'])
