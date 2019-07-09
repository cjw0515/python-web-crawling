import sqlite_db
from dlimage import image_download as imgd
from dlimage import get_simillarity as get_sim
from common import get_items_ten_api as ten_api
import constant as const
from bestitem_1300k import BestItem
from search_result import SearchResultItem
import re
import random
import shutil
import textdistance


class MatchItems:

    def __init__(self):
        self.items = []
        self.ten_items = []
        self.search_result = []

    def set_items(self, sql, db):
        db = sqlite_db.SqliteDatabase(db)
        items = db.query(sql)

        for item in items:
            tmp_obj: BestItem = BestItem(
                category=item[1],
                rank=item[2],
                imageURL=item[3],
                itemCode=item[4],
                brand=item[5],
                itemName=item[6],
                price=item[7],
                salePrice=item[8],
                numOfReview=item[9],
                numOfLike=item[10]
            )
            self.items.append(tmp_obj)

    def set_search_result(self, keyword_container, item_id, category, min: int, max: int):
        result_obj = {
            'cnt': 0,
            'itemid': item_id,
            'keyword': '',
            'category': category,
            'result_items': []
        }
        if len(keyword_container) == 0:
            self.search_result.append(result_obj)
            return
        keyword = keyword_container.pop()
        result_obj['keyword'] = keyword
        result_arr = self.search(keyword=keyword)
        cnt = int(result_arr[0].replace("\r", ""))
        result_obj['cnt'] = cnt

        if cnt < min or cnt > max:
            # 재귀
            self.set_search_result(keyword_container, item_id, category, min, max)
            return

        item_arr = []
        for idx in range(1, len(result_arr)):
            tmp_items = result_arr[idx]
            col = tmp_items.split("||")
            if len(col) == 1:
                continue
            tmp_item: SearchResultItem = SearchResultItem(
                itemCode=col[0],
                ItemName=col[1],
                brandEName=col[2],
                brandKName=col[3],
                imgURL1=col[4],
                imgURL2=col[5],
                itemTag=col[6]
            )
            item_arr.append(tmp_item)

        result_obj['result_items'] = item_arr
        self.search_result.append(result_obj)

    def item_img_download(self):
        for item in self.items:
            imgd(item.imageURL, const.IMG_1300k_DIR
                 , "{category}_{itemid}".format(category=item.category, itemid=item.itemCode))

    def search_img_download(self):
        def tmp_fn(obj):
            return obj['cnt'] != 0
        for result_objs in list(filter(tmp_fn, self.search_result)):
            for item in result_objs['result_items']:
                imgd(item.imgURL1
                     , const.IMG_10x10_DIR
                     , "{category}_{itemid}_{tencode}_{order}".format(
                        category=result_objs['category']
                        , itemid=result_objs['itemid']
                        , tencode=item.itemCode
                        , order=1
                        ))

                if item.imgURL2 != '':
                    imgd(item.imgURL2
                         , const.IMG_10x10_DIR
                         , "{category}_{itemid}_{tencode}_{order}".format(
                            category=result_objs['category']
                            , itemid=result_objs['itemid']
                            , tencode=item.itemCode
                            , order=2
                            ))

    def search(self, keyword):
        api_result = ten_api(keyword)
        result_arr = api_result.split("\n")

        return result_arr

    def get_shuffled_keywords(self, brand_name: str, item_name: str, num_add: int):
        item_name_arr = item_name.split(" ")
        if len(item_name_arr) < 2:
            return []

        added_text_arr = []
        while len(added_text_arr) < len(item_name_arr):
            random.shuffle(item_name_arr)
            ran_num = random.randint(1, num_add)

            added_text = ""
            is_exists = False

            for i in range(0, ran_num):
                added_text = added_text + " " + item_name_arr[i]

            added_text = brand_name + added_text
            for j in range(0, len(added_text_arr)):
                if added_text_arr[j] == added_text:
                    is_exists = True
                    break
            if not is_exists:
                added_text_arr.append(added_text)

        return added_text_arr


if __name__ == "__main__":
    match = MatchItems()

    match.set_items(sql="""
           select *
         from best100_1300k
        where category = "전체"
           """, db='../1300k_best.db')

    for item in match.items:
        keyword_container = [
            item.brand,
            item.itemName
        ]
        keyword_container = match.get_shuffled_keywords(brand_name=item.brand
                                                        , item_name=item.itemName
                                                        , num_add=2) + keyword_container

        match.set_search_result(keyword_container=keyword_container
                                , item_id=item.itemCode
                                , category=item.category
                                , min=1
                                , max=30)
    #
    # match.search_img_download()



    def tmp_fn(obj):
        return obj['cnt'] == 0
    result = list(filter(tmp_fn, match.search_result))
    for item in match.search_result:
        print(item)
    print(len(match.search_result))
    print(len(result))






