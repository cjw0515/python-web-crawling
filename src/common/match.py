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
from os.path import splitext


class MatchItems:

    def __init__(self):
        self.items = []
        self.ten_items = []
        self.search_result = []
        self.keyword_cont_list = []

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

    def set_keyword_cont_list(self, item_code, keyword_container: list):
        keyword_cont_obj = {
            'item_code': item_code,
            'keyword_cont': keyword_container
        }
        self.keyword_cont_list.append(keyword_cont_obj)

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

        return matched_items

    @staticmethod
    def match_imgs(img_arr1: list, img_arr2: list, itemid:int, category:str):
        result_arr = []
        name_format = "img_{category}_{itemid}".format(category=category, itemid=itemid)

        for item_img in img_arr1:
            if item_img.startswith(name_format):
                for ten_img in img_arr2:
                    if ten_img.startswith(name_format):
                        # 비교
                        result = sim(os.path.join(const.IMG_1300k_DIR, item_img)
                                     , os.path.join(const.IMG_10x10_DIR, ten_img))
                        print(result)
                        if result > 0.9:
                            result_arr.append({int(splitext(item_img)[0].split("_")[2]): ten_img.split("_")[3]})
                            print(result_arr)

        return result_arr

    def match_item_names(self):
        result_arr = []

        for result in self.search_result:
            if result['cnt'] < 1:
                continue
            for item in result['result_items']:
                if string_match(result['item_name'], item.ItemName) > 0.9:
                    result_arr.append({result['itemid']: item.itemCode})

        return result_arr



if __name__ == "__main__":
    match = MatchItems()

    match.set_items(sql="""
           select *
         from best100_1300k
        where category = "전체"
           """, db='../1300k_best.db')

    # print(match.match_items())

    # print(common.string_match('공백 세탁조 크리너 3+1', '공백 세탁조 크리너 (4매입) 3+1'))


    # for item in match.items:
    #     keyword_container = [
    #         item.brand,
    #         item.itemName
    #     ]
    #     keyword_container = match.get_shuffled_keywords(brand_name=item.brand
    #                                                     , item_name=item.itemName
    #                                                     , num_add=2) + keyword_container
    #
    #     match.set_search_result(keyword_container=keyword_container
    #                             , item_id=item.itemCode
    #                             , item_name=item.itemName
    #                             , category=item.category
    #                             , min=1
    #                             , max=30)

    # print(match.match_item_names())
    result1 = [{215024411696: '1921111'}, {215024691237: '2100659'}, {215024343576: '1620286'},
         {215024596347: '2238780'}, {215024452104: '2114323'}, {215024452104: '2114323'},
         {215023217837: '1507933'}, {215024596618: '2246341'}, {215024278659: '1974315'},
         {215023033246: '1429847'}, {215023108566: '1428513'}, {215022109166: '1013844'},
         {215024643100: '2283244'}, {215024663167: '2306758'}, {215024702984: '2339102'},
         {215024278614: '1974138'}, {215024218432: '1930373'}, {215024218432: '1930373'},
         {215024640397: '2286228'}, {215024772581: '2406132'}, {215024372307: '2006537'},
         {215024591220: '2246292'}, {215024702485: '2317055'}, {215023586975: '1932495'},
         {215024714845: '2356025'}, {215023934931: '1781435'}, {215022422844: '1164840'},
         {215024476528: '2132580'}, {215024723940: '2363172'}, {215023171402: '1488741'},
         {215023163657: '1486018'}, {215024666376: '2306678'}, {215023816257: '1731755'},
         {215024255564: '1801285'}]
    result2 = [{215024596347: '2238780'}, {215023108592: '1641555'}, {215024255565: '1801285'}, {215024255565: '1567371'},
     {215024255565: '1579493'}, {215024596618: '2246341'}, {215024278659: '1974140'}, {215023033246: '1429847'},
     {215023033246: '2053006'}, {215022109166: '1013844'}, {215023513814: '2074801'}, {215024643100: '2283244'},
     {215024663167: '2306758'}, {215024695388: '2324114'}, {215023108616: '1428513'}, {215024278614: '1974138'},
     {215024218432: '1930372'}, {215024218432: '1930373'}, {215024772581: '2406132'}, {215024372307: '2006538'},
     {215024372307: '2006537'}, {215022422844: '1164840'}, {215024476528: '2132580'}, {215024723940: '2363172'},
     {215023163657: '1486018'}, {215024666376: '2306678'}, {215024557759: '2197891'}, {215023816257: '1731755'},
     {215023807450: '1856268'}, {215024502011: '2155759'}, {215024255564: '1801285'}, {215024255564: '1567371'}]

    tot_rst = result1 + result2
    print(tot_rst)
    print(set(tot_rst))
    print({215023807450: '1856268'} == {215023807450: '1856268'})

    # match.search_img_download()

    # file_list1 = os.listdir(const.IMG_1300k_DIR)
    # file_list2 = os.listdir(const.IMG_10x10_DIR)
    # # print(file_list1)
    # for file in file_list1:
    #     file_name = splitext(file)[0]
    #     ten_item_id = 0

        # if file_name.startswith('img_전체_215022109166'):
        #     print()
    #
    #
    # def tmp_fn(obj):
    #     return obj['cnt'] == 0
    # result = list(filter(tmp_fn, match.search_result))
    # for item in match.search_result:
    #     print(item)
    # print(len(match.search_result))
    # print(len(result))






