#!../bin/python
# coding: utf-8

import sys
import unittest
from HTMLTestRunner import HTMLTestRunner
from cases.test_amenity import AmenityTestCase
from cases.test_ubike import UbikeTestCase

# 防止中文錯誤
reload(sys)
sys.setdefaultencoding('utf8')

# 產生 HTML 版本的測試報表
mySuite = unittest.TestSuite()
mySuite.addTest(unittest.makeSuite(AmenityTestCase))
mySuite.addTest(unittest.makeSuite(UbikeTestCase))
runner = HTMLTestRunner(title='OSM.TW 測試報告', description='台灣開放街圖資料完整性測試報告')
runner.run(mySuite)
