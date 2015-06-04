# coding: utf-8

import psycopg2
import psycopg2.extras
import unittest

class OsmTestCase(unittest.TestCase):

	@classmethod
	def setUp(self):
		self.con = psycopg2.connect(host='127.0.0.1', user='osm', password='osm4326', database='osm')
		self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

	@classmethod
	def tearDown(self):
		self.cur.close()
		self.con.close()

	## 查詢，返回 list > DictRow 結構
	def query(self, sql):
		cur = self.cur
		cur.execute(sql)
		return cur.fetchall()

	## 產生 osm_id 欄位的列舉字串，太多筆的時候顯示 ...
	def get_osmid_summary(self, rows, limit=3):
		summary = []
		for r in rows:
			summary.append('%d' % r['osm_id'])
			if len(summary)==limit: break

		summary = ', '.join(summary)
		if len(rows)>limit:
			morecnt = len(rows) - limit
			summary = summary + ', 還有 %d 筆 ...' % morecnt
		return summary
