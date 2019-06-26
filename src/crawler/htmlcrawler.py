import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite_db


def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)
    driver.implicitly_wait(3)
    html = driver.page_source
    driver.quit()

    return html


def insert_data(db_path, data):
    with sqlite_db.SqliteDatabase(db_path) as db:
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
        )values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.execute_many(insert_table_sql, data)


def crawl_1300k_best(html):
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.select('.gc_glst > li')
    item_arr = []

    for item in item_list:
        category =  '1'
        rank = item.select('.ico_rank')[0].text
        image_URL = item.select('.gimg')[0].attrs['gimg']
        item_code = item.select('.gimg')[0].attrs['gno']
        brand = item.select('.a_bname')[0].text
        item_name = item.select('.a_gname')[0].text
        price = 648
        sale_price = 3523
        num_of_review = 3235
        num_of_like = 2342

        tmp_obj = (
            category
            , rank
            , image_URL
            , item_code
            , brand
            , item_name
            , price
            , sale_price
            , num_of_review
            , num_of_like
        )
        item_arr.append(tmp_obj)

    return item_arr




# if __name__ == "__main__":
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