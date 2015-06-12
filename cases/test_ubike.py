# coding: utf-8

from cases.osmtest import OsmTestCase
from chainsrc.ubike import UbikeSource

# 不顯示 stack trace
__unittest = True

## U-bike 圖資測試
class UbikeTestCase(OsmTestCase):

	## 取 U-bike 站點資料 (一次性)
	@classmethod
	def setUpClass(cls):
		super(cls, UbikeTestCase).setUpClass()
		UbikeTestCase.src = UbikeSource()

	## 測試新站點
	def test01_new(self):
		points = UbikeTestCase.src.getNewPoints()
		if len(points)>0:
			msg = u'需要新增 U-bike 站 (%d)' % len(points)
			for p in points:
				msg = msg + '\n%s %s' % (p['ref'], p['name'])
			self.fail(msg)

	## 測試變更點
	def test02_changed(self):
		points = UbikeTestCase.src.getChangedPoints()
		if len(points)>0:
			msg = u'需要修改 U-bike 站 (%d)' % len(points)
			for p in points:
				msg = msg + '\n[%s] %s %s' % (p['osm_id'], p['ref'], p['name'])
			self.fail(msg)

	## 測試消失點
	def test03_disappeared(self):
		points = UbikeTestCase.src.getDisappearedPoints()
		if len(points)>0:
			msg = u'需要移除 U-bike 站 (%d)' % len(points)
			for p in points:
				msg = msg + '\n[%s] %s %s' % (p['osm_id'],p['ref'], p['name'])
			self.fail(msg)
