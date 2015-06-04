# coding: utf-8

from cases.osmtest import OsmTestCase
from chainsrc.ubike import UbikeSource

# 不顯示 stack trace
__unittest = True

class UbikeTestCase(OsmTestCase):

	@classmethod
	def setUp(self):
		super(UbikeTestCase,self).setUp()
		self.src = UbikeSource()

	@classmethod
	def tearDown(self):
		super(UbikeTestCase,self).tearDown()

	def test01_new(self):
		points = self.src.getNewPoints()
		if len(points)>0:
			msg = '需要新增 U-bike 站 (%d)' % len(points)
			for p in points:
				msg = msg + '\n%s %s' % (p['ref'], p['name'])
			self.fail(msg)

	def test02_changed(self):
		points = self.src.getChangedPoints()
		if len(points)>0:
			msg = '需要修改 U-bike 站 (%d)' % len(points)
			for p in points:
				msg = msg + '\n[%s] %s %s' % (p['osm_id'], p['ref'], p['name'])
			self.fail(msg)

	def test03_disappeared(self):
		points = self.src.getDisappearedPoints()
		if len(points)>0:
			msg = '需要移除 U-bike 站 (%d)' % len(points)
			for p in points:
				msg = msg + '\n[%s] %s %s' % (p['osm_id'],p['ref'], p['name'])
			self.fail(msg)
