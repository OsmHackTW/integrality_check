# coding: utf-8

import osmtest

class AmenityTestCase(osmtest.OsmTestCase):

	## point 命名有廁所，但是 amenity 為 NULL
	def test01_toilets_without_amenity(self):
		sql = "SELECT osm_id,name,amenity FROM planet_osm_point WHERE name LIKE '%廁所%' AND amenity IS NULL"
		rows = self.query(sql)
		if len(rows)>0:
			summary = self.get_osmid_summary(rows)
			msg = '找到沒標記 amenity 的廁所 (%s)' % summary
			self.fail(msg)

	## amenity 為 toilet
	def test02_toilets_as_toilet(self):
		sql = "SELECT osm_id,name,amenity FROM planet_osm_point WHERE amenity LIKE '%toilet%' AND amenity!='toilets'"
		rows = self.query(sql)
		if len(rows)>0:
			summary = self.get_osmid_summary(rows)
			msg = '找到 amenity 誤標記成 toilet 的廁所 (%s)' % summary
			self.fail(msg)
