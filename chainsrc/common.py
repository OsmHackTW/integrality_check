# coding: utf-8

import abc
import json
import psycopg2
import psycopg2.extras

## 連鎖企業 POI 資料蒐集架構
#  取得連鎖企業的最新 POI，以及和 PostGIS 比對 POI 是否需要 新增/修改/刪除
#
#  @todo 設計 cache 機制，用 SQLite
#
class ChainSource(object):

	## 初始動作
	#  (載入 POI 以及 POI 狀態分類)
	def __init__(self):
		self.loaded = False

		# 注意!! 這組不能放在外面，不然會變成 static members
		self.points = []
		self.points_new = []
		self.points_changed = []
		self.points_unchanged = []
		self.points_disappeared = []

		self.con = psycopg2.connect(host='127.0.0.1', user='osm', password='osm4326', database='osm')
		self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		self.loadLatestPoints()

		# POI 分類
		if self.loaded:
			for p in self.points:
				status = self.getPointStatus(p)
				tmap = {
					'new':       self.points_new,
					'changed':   self.points_changed,
					'unchanged': self.points_unchanged
				}
				tmap[status].append(p)
			self.loadDisappearedPoints();

		self.cur.close()
		self.con.close()

	## 查詢
	#  (給子類別用，節省時間)
	def query(self, sql, single=False):
		cur = self.cur
		cur.execute(sql)
		if single:
			return cur.fetchone()
		else:
			return cur.fetchall()

	## 取得摘要資訊
	def summary(self):
		cnt = (
			len(self.points_new),
			len(self.points_changed),
			len(self.points_disappeared),
			len(self.points_unchanged)
		)
		msg = '新增 %d, 修改 %d, 撤點 %d, 不變 %d' % cnt
		return msg

	## 同步到 OSM Server
	def sync(self):
		pass

	## 載入資料源，也就是砍站動作
	#  (子類別實作，負責變更 self.loaded 與 self.points)
	@abc.abstractmethod
	def loadLatestPoints(self): pass

	## 載入已撤點清單
	#  (子類別實作，負責變更 self.points_disappeared)
	#  注意!! 除了撤點的可能性以外，也可能是重複標記
	@abc.abstractmethod
	def loadDisappearedPoints(self): pass

	## 檢查單點是否已存在
	#  (子類別實作，如果是已存在的點要順便把 osm_id 塞進 point)
	@abc.abstractmethod
	def getPointStatus(self, point): pass

	## 是否已載入
	def isLoaded(self):
		return self.loaded

	## 取得所有資料源的點
	def getPoints(self):
		return self.points

	## 取得新點
	#  (資料源有，但是 PostGIS 沒有)
	def getNewPoints(self):
		return self.points_new

	## 取得變更點
	#  (資料源與 PostGIS 都有)
	def getChangedPoints(self):
		return self.points_changed

	## 取得現有點
	#  (資料源與 PostGIS 都有)
	def getUnchangedPoints(self):
		return self.points_unchanged

	## 取得消失點
	#  (資料源沒有，但是 PostGIS 有)
	def getDisappearedPoints(self):
		return self.points_disappeared
