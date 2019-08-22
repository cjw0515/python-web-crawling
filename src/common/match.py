import sqlite_db
from dlimage import image_download as imgd
from dlimage import get_simillarity as sim
from common import get_items_ten_api as ten_api
from common import string_match
import constant as const
from bestitem_1300k import BestItem
from search_result import SearchResultItem
import random
import os
import re
from os.path import splitext
from mysql_db import MysqlDatabase


class MatchItems:

    def __init__(self, img_similarity: float = 0.9, text_similarity: float = 0.9):
        self.items = []
        self.ten_items = []
        self.search_result = []
        self.matched_items = set()
        self.IMG_SIMILARITY = img_similarity
        self.TEXT_SIMILARITY = text_similarity

        # self.keyword_cont_list = []

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

    def set_items2(self, category):
        my_db = MysqlDatabase()
        my_db.create_1300k_table()
        items = my_db.select_1300k_data(category)

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

    def set_search_result(self, keyword_container, item_id, item_name, category, min: int, max: int):
        result_obj = {
            'cnt': 0,
            'itemid': item_id,
            'item_name': item_name,
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
            self.set_search_result(keyword_container, item_id, item_name, category, min, max)
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

    # def set_keyword_cont_list(self, item_code, keyword_container: list):
    #     keyword_cont_obj = {
    #         'item_code': item_code,
    #         'keyword_cont': keyword_container
    #     }
    #     self.keyword_cont_list.append(keyword_cont_obj)
    def set_matched_items(self, matched_results: list):
        self.matched_items.update(set(matched_results))

    @staticmethod
    def search(keyword):
        api_result = ten_api(keyword)
        result_arr = api_result.split("\n")

        return result_arr

    @staticmethod
    def get_shuffled_keywords(brand_name: str, item_name: str, num_add: int):
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

    def match_items(self):
        ten_img_arr = os.listdir(const.IMG_10x10_DIR)
        s1300k_img_arr = os.listdir(const.IMG_1300k_DIR)
        matched_items = []

        for item in self.items:
            itemid_1300k = item.itemCode
            category = item.category
            matched_items += self.match_imgs(img_arr1=s1300k_img_arr
                                             , img_arr2=ten_img_arr
                                             , itemid=itemid_1300k
                                             , category=category)

        self.set_matched_items(matched_items)

    def match_imgs(self, img_arr1: list, img_arr2: list, itemid: int, category: str):
        result_arr = []
        name_format = "img_{category}_{itemid}".format(category=category, itemid=itemid)
        for item_img in img_arr1:
            if item_img.startswith(name_format):
                for ten_img in img_arr2:
                    if ten_img.startswith(name_format):
                        # 비교
                        result = sim(os.path.join(const.IMG_1300k_DIR, item_img)
                                     , os.path.join(const.IMG_10x10_DIR, ten_img))
                        if result > self.IMG_SIMILARITY:
                            result_arr.append((int(splitext(item_img)[0].split("_")[2]), ten_img.split("_")[3]))

        return result_arr

    def match_item_names(self):
        result_arr = []

        for result in self.search_result:
            if result['cnt'] < 1:
                continue
            for item in result['result_items']:
                if string_match(result['item_name'], item.ItemName) > self.TEXT_SIMILARITY:
                    result_arr.append((int(result['itemid']), item.itemCode))

        self.set_matched_items(result_arr)

    def update_matched_data(self, category):
        with sqlite_db.SqliteDatabase(const.DB_1300K_BEST_PATH) as db:
            for item in self.matched_items:
                item_code = item[0]
                ten_code = item[1]
                items = db.query(sql="""
                   select MatchedItem
                     from best100_1300k
                    where category = ?
                      and ItemCode = ?
                """, params=(category, item_code))

                if len(items) > 0:
                    if items[0][0] != None:
                        tmp_itemid = str(items[0][0]) + "," + str(ten_code)
                    else:
                        tmp_itemid = str(ten_code)

                    db.execute(sql="""
                                    update best100_1300k
                                       set MatchedItem = ?
                                     where category = ?
                                       and ItemCode = ?
                                    """, params=(tmp_itemid, category, item_code))

    def update_matched_data2(self, category):

        my_db = MysqlDatabase()
        my_db.create_1300k_table()

        for item in self.matched_items:
            item_code = item[0]
            ten_code = item[1]
            items = my_db.select_1300k_mached_data(category, item_code)
            print(items)

            if len(items) > 0:
                if items[0][0] != None:
                    tmp_itemid = str(items[0][0]) + "," + str(ten_code)
                else:
                    tmp_itemid = str(ten_code)

                # 업데이트
                my_db.update_1300k_matched_data(category, item_code, tmp_itemid)

    def run(self, category):
        # 아이템 셋
        print("상품 셋...")
        # sqlite
        #
        # self.set_items(sql="""
        #        select *
        #      from best100_1300k
        #     where category = "{category}"
        #        """.format(category=category), db=const.DB_1300K_BEST_PATH)

        # mysql
        self.set_items2(category)

        # 아이템 검색 결과 셋
        print("검색중...")
        for item in self.items:
            keyword_container = [
                item.brand,
                item.itemName
            ]
            keyword_container = self.get_shuffled_keywords(brand_name=item.brand
                                                            , item_name=item.itemName
                                                            , num_add=2) + keyword_container

            self.set_search_result(keyword_container=keyword_container
                                    , item_id=item.itemCode
                                    , item_name=item.itemName
                                    , category=item.category
                                    , min=1
                                    , max=30)

        # 이미지 다운로드
        self.item_img_download()
        self.search_img_download()

        # 아이템 매칭
        print("이미지 매칭중...")
        self.match_items()
        print("아이템 이름 매칭중...")
        self.match_item_names()

        print(self.matched_items)

        # 매치상품 업데이트
        print("상품 업데이트...")
        self.update_matched_data2(category)
        return True

if __name__ == "__main__":
    # print(string_match('[무료배송] 바디럽 마약빈백', '바디럽 마약빈백'))
    teststring = '[무료배송] BOXER BRIEFS-LOW RISE BASIC PACK [ 3SET ]'
    # result = re.search('무료배송', teststring)
    # result = re.search('\\[(.*?)\\]', teststring)
    result = re.sub('\\[(.*?)\\]', '', teststring).strip()
    print(result)





