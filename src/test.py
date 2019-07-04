import sqlite_db
import bestitem_1300k
import textdistance
import requests
import cv2 as cv
import numpy as np
import common as com
import shutil
import dlimage as dimg

if __name__ == '__main__':
    sql = """
    select *
  from best100_1300k
    """
    db = sqlite_db.SqliteDatabase('1300k_best.db')

    result = db.query(sql)
    img_url = result[2][3]
    dimg.image_download(img_url, 'images/1300k/', '4654')

    # print(result[0][3])
    # print(textdistance.jaro.normalized_similarity('고온어도시락현미밥식단시즌3 12팩', '고온어도시락 현미밥식단 시즌3'))
    # api_result = com.get_items_searchapi('양산')
    # print(api_result)

    # items = []
    # items = api_result.split("\n")
    # print(items[0])