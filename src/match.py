import sqlite_db
from dlimage import image_download as imgd
from common import get_items_ten_api as ten_api
import constant as const


def main():
    sql = """
      select category
           , brand
           , itemName
           , itemCode
           , imageURL           
    from best100_1300k
   where category = "전체" 
      """
    db = sqlite_db.SqliteDatabase('1300k_best.db')
    result = db.query(sql)
    for item in result:
        brand = item[1]
        item_name = item[2]
        imgURL = item[4]

        api_result = ten_api(item_name)

        result_items = []
        result_items = api_result.split("\n")

        if int(result_items[0].replace("\r", "")) > 0:
            print("*" * 20)
            print("keyword : {keyword}".format(keyword=item_name))
            print("imgURL : {imgURL}".format(imgURL=imgURL))
            print("result1 : {result}".format(result=result_items[0]))
            print("result2 : {result}".format(result=result_items[1]))
            print("result3 : {result}".format(result=result_items[2]))

        # img_url = item[3]
        # category = item[1]
        # rank = item[2]
        # imgd(img_url, const.IMG_1300k_DIR, "{category}_{rank}".format(category=category,rank=rank))


if __name__ == "__main__":
    main()