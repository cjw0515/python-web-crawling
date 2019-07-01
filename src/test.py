import sqlite_db
import bestitem_1300k

if __name__ == '__main__':
    sql = """
    select *
  from best100_1300k

    """
    db = sqlite_db.SqliteDatabase('1300k_best.db')
    # tmp_obj = bestitem_1300k.BestItem(
    #     category=_category,
    #     rank=_rank,
    #     imageURL=_imageURL,
    #     itemCode=_itemCode,
    #     brand=_brand,
    #     itemName=_itemName,
    #     price=_price,
    #     salePrice=_salePrice,
    #     numOfReview=_numOfReview,
    #     numOfLike=_numOfLike
    # )
    result = db.query(sql)
    img_url = result[0][3]
    
    # print(result[0][3])
