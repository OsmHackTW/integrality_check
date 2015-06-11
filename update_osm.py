#!../bin/python
# coding: utf-8
#
# 台灣 OSM 圖資自動更新程式，會自動檢查更新，有更新時下載，並且匯入到 PostGIS
#
# 系統需求:
# * wget
# * osm2pgsql 並且內含 PBF 圖資格式支援
#
# 測試環境:
# * Ubuntu 14.04.1 LTS
# * OS X Yosemite 10.10.3

import os
import hashlib
from os.path import expanduser

RETRY_LIMIT = 3
HOME        = expanduser("~")

# PostgreSQL 參數
# TODO: 以後要改成從安全的設定檔讀取
DB_HOST = '127.0.0.1'
DB_USER = 'osm'
DB_NAME = 'osm'

# 圖資參數
MAP_EXTRACT = 'taiwan-latest.osm.pbf'
URL_MD5     = 'http://download.geofabrik.de/asia/%s.md5' % MAP_EXTRACT
URL_FILE    = 'http://download.geofabrik.de/asia/%s' % MAP_EXTRACT
MD5_PREV    = '%s/osm-data/prev.md5' % HOME
MD5_CURR    = '%s/osm-data/curr.md5' % HOME
LOCAL_FILE  = '%s/osm-data/%s' % (HOME, MAP_EXTRACT)

## 檢查是否有更新圖資
def isUpdated():
    # 先下載新的 MD5
    os.system('wget -nv %s -O %s' % (URL_MD5, MD5_CURR))

    # 檢查是否有舊的 MD5 與圖資，如果沒有舊記錄，就視為要更新
    if os.path.isfile(MD5_PREV)   is False: return True
    if os.path.isfile(LOCAL_FILE) is False: return True

    # 新舊 MD5 比對，如果 MD5 不同就視為要更新
    ret = os.system('diff %s %s' % (MD5_PREV, MD5_CURR))
    if ret != 0: return True

    # MD5 相同，不用更新
    return False

## 更新圖資，並且檢查 MD5，如果檔案完整就回傳 True
#  (注意! 因為 OSX 缺少 md5sum 指令，所以統一用 hashlib 計算 MD5 摘要)
def updateOSM():
    os.system('wget -nv %s -O %s' % (URL_FILE, LOCAL_FILE))        # 下載圖資
    md5sum = hashlib.md5(open(LOCAL_FILE,'rb').read()).hexdigest() # 比對 MD5
    ret = os.system('grep %s %s' % (md5sum, MD5_CURR))             
    if ret == 0:
        os.system('mv -f %s %s' % (MD5_CURR, MD5_PREV))            # 新 MD5 轉換為舊 MD5
        return True
    return False

if isUpdated():
    # 下載圖資
    cnt = 0
    while(updateOSM() is False):
        cnt = cnt + 1
        if cnt > RETRY_LIMIT:
            print('圖資下載失敗')
            exit(1)
    print('圖資下載成功，匯入到 PostGIS')

    # 匯入到 PostgreSQL
    # 使用較保守的參數，避免在便宜的雲端空間撐爆記憶體
    command = '''
        osm2pgsql --cache 256 --cache-strategy sparse \
            -l -H %s -U %s -d %s %s
    '''
    params  = (DB_HOST, DB_USER, DB_NAME, LOCAL_FILE)
    os.system(command % params)
    print('匯入完成')

    exit(0)
else:
    print('圖資沒更新，不需要下載')
    exit(0)
