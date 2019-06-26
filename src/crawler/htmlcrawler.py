import requests
import sqlite3 as lite
from bs4 import BeautifulSoup
from selenium import webdriver
import bestitem_1300k
import sqlite_db


def crawl_html(url, get_params=(), request_headers={}):
    response = requests.get(url)
    html = response.text
    print(html)


if __name__ == "__main__":
    # response = requests.get("http://www.1300k.com/shop/best/best.html?f_bid=HD4001")
    # print(response.encoding)
    # print(response.text)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get('http://www.1300k.com/shop/best/best.html?f_bid=HD4001')
    driver.implicitly_wait(3)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    item_list = soup.select('.gc_glst > li')

    item_arr = []

    for item in item_list:
        _category =  '1'
        _rank = item.select('.ico_rank')[0].text
        _imageURL = item.select('.gimg')[0].attrs['gimg']
        _itemCode = item.select('.gimg')[0].attrs['gno']
        _brand = item.select('.a_bname')[0].text
        _itemName = item.select('.a_gname')[0].text
        _price = 648
        _salePrice = 3523
        _numOfReview = 3235
        _numOfLike = 2342

        tmp_obj = (
            _category
            , _rank
            , _imageURL
            , _itemCode
            , _brand
            , _itemName
            , _price
            , _salePrice
            , _numOfReview
            , _numOfLike
        )

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

        item_arr.append(tmp_obj)

    with sqlite_db.SqliteDatabase('test.db') as db:
        create_table_sql = """
        create table if not exists best100_1300k(
            "Idx"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "Category"	TEXT,
            "Rank"	INTEGER,
            "ImageURL"	TEXT,
            "ItemCode"	INTEGER,
            "Brand"	TEXT,
            "ItemName"	TEXT,
            "Price"	INTEGER,
            "SalePrice"	INTEGER,
            "NumOfReview"	INTEGER,
            "NumOfLike"	INTEGER
        )
        """
        db.execute(create_table_sql)
        insert_table_sql = """
        insert into best100_1300k(
             Category
            , Rank
            , ImageURL
            , ItemCode
            , Brand
            , ItemName
            , Price
            , SalePrice
            , NumOfReview
            , NumOfLike
        )values(
             ?
            , ?
            , ?
            , ?
            , ?
            , ?
            , ?
            , ?
            , ?
            , ?
        )
        """
        db.execute_many(insert_table_sql, item_arr)
    # print(len(item_arr))

    # print(item_list[0].select('.gimg')[0].attrs['gimg']) #.select('.gimg').attrs
    # print(type(item_list[0].text))

    # brand_name = soup.select('.bst .a_bname')
    # item_name = soup.select('.bst .a_gname')
    # for item in brand_name:
    #     print(item.text)
    #
    # for item in item_name:
    #     print(item.text)