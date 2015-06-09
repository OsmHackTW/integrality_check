# coding: utf-8

import os
import urllib
import json
from pprint import pprint
from chainsrc.common import ChainSource
from osmapi import OsmApi

## Ubike 圖資蒐集比對程式
#
# * 撤點功能暫不設計，因為很多新北市的點還是會算在台北市裡面，會不小心被撤掉
#
class UbikeSource(ChainSource):

	source_name = u'YouBike 租借站'

	## 載入 U-bike 資料源
	#  (去官網砍站)
	def loadLatestPoints(self):
		url = 'http://taipei.youbike.com.tw/cht/f12.php?loc=taipei'
		cmd = 'wget \'%s\' -q -O - | head -n 196 | tail -n 1 | grep  -o "\'.*\'"' % url

		# 資料結構化
		# trim > url decode > json decode
		p = os.popen(cmd,'r',8192)
		c = p.read().strip('\'\n')
		p.close()
		c = urllib.unquote(c)
		c = json.loads(c)
		self.loaded = True

		for key, item in c.items():
			point_dict = {
				'lat':      item['lat'],
				'lon':      item['lng'],
				'name':     item['sna'],
				'ref':      item['sno'],
				'capacity': item['tot'],
				'brand':    u'YouBike',
				'opertor':  u'巨大機械工業(股)',
				'network':  u'YouBike 微笑單車'
			}
			self.points.append(point_dict)

	## 取出已消失的 U-bike 點
	#  (PostGIS 有資料，但是資料源卻無資料)
	def loadDisappearedPoints(self):
		# 全台北市 U-bike 點
		sql = '''
			SELECT osm_id, name, ref, ST_Y(way) lat, ST_X(way) lng FROM planet_osm_point
			WHERE amenity='bicycle_rental' AND ref IS NOT NULL
			AND ST_Contains((SELECT way FROM planet_osm_polygon WHERE name='臺北市'), way)
		'''
		points = self.query(sql)

		# 到 changed, unchanged 點比對 osm_id
		# 如果完全沒有 match 表示該點應該已消失
		for p_gis in points:
			disappeared = True
			p_gis['name'] = unicode(p_gis['name'], 'utf-8')
			osm_id = p_gis['osm_id']

			for p_src in self.points_changed:
				if p_src['osm_id'] == osm_id:
					disappeared = False

			if disappeared:
				for p_src in self.points_unchanged:
					if p_src['osm_id'] == osm_id:
						disappeared = False

			if disappeared:
				self.points_disappeared.append(p_gis)

	## 檢查指定點的資料狀態
	#
	#  @return 資料狀態 'new','changed','unchanged'
	#
	def getPointStatus(self, point):
		sql = '''
			SELECT osm_id, name, ref, amenity, brand, operator, ST_AsText(way) loc
			FROM planet_osm_point
			WHERE ST_Distance(way,ST_GeomFromText('POINT(%s %s)',4326),true)<5
			AND amenity='bicycle_rental'
		''' % (point['lon'], point['lat'])

		row = self.query(sql, True)
		if row is None:
			return 'new'

		# 確定該點存在，記錄 osm_id 供事後產生 UPDATE SQL 使用
		point['osm_id'] = row['osm_id']

		changed = False
		for k in ['name', 'ref', 'brand', 'operator']:
			field = u'' if row[k] is None else unicode(row[k],'utf-8')
			if field!=point[k]:
				return 'changed'

		return 'unchanged'
