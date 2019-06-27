import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite_db
import common_fn

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
            "NumOfLike"	INTEGER,
            "RegDate" DATETIME
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
            , RegDate
        )values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, DATETIME('NOW'))
        """
        db.execute_many(insert_table_sql, data)


def crawl_1300k_best(html):
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.select('.gc_glst > li')

    # 같은 용도의 객체이나, 마크업이 다른것이 소수일 경우 메인로직에서 연산을 줄이기 위한 별도 처리과정 필요

    list_for_replace = [
        {'tag': 'span', 'old': 'gc_gpr_del', 'new': 'gpr_del'},
        {'tag': 'span', 'old': 'gc_gpr_sale', 'new': 'gpr_sale'}
    ]
    best2to5 = replace_attr(soup.select('.bst_rank .rank_bx2 li'), list_for_replace)
    bset1 = replace_attr(soup.select('.bst_rank .rank_bx1'), list_for_replace)

    # best1상품 태그 삽입
    new_tag1 = soup.new_tag('span', attrs={"class": "ico_rank"})
    new_tag1.string = "1"
    new_tag2 = soup.new_tag('span', attrs={'class': 'gimg', 'gimg': 'http://imgc.1300k.com/aaaaaib/goods/215024/59/215024596347.jpg?3'})



    bset1 = insert_tag(bset1, [
        new_tag1,
        new_tag2
    ])
    best2to5 = insert_tag(best2to5, [
        new_tag2
    ])

    item_list = item_list + best2to5
    item_list = item_list + bset1

    item_arr = []
    tmp_price_dic = {'Price': None, 'SalePrice': None}

    # print(item_list)

    # for item in item_list:
    #     category =  '1'
    #     rank = item('span', {'class': 'ico_rank'})[0].text
    #     image_URL = item('span', {'class': 'gimg'})[0].attrs['gimg']
    #     item_code = item('span', {'class': 'gimg'})[0].attrs['gno']
    #     brand = item('a', {'class': 'a_bname'})[0].text
    #     item_name = item('a', {'class': 'a_gname'})[0].text
    #     tmp_price_dic = get_item_price(item('span', {'class': 'gprice'})[0])
    #     price = tmp_price_dic['Price']
    #     sale_price = tmp_price_dic['SalePrice']
    #     num_of_review = 3235
    #     num_of_like = 2342
    #
    #     tmp_obj = (
    #         category
    #         , rank
    #         , image_URL
    #         , item_code
    #         , brand
    #         , item_name
    #         , price
    #         , sale_price
    #         , num_of_review
    #         , num_of_like
    #     )
    #     item_arr.append(tmp_obj)
    #
    # return item_arr


def insert_tag(obj, new_tag_list):
    obj[0].append(new_tag_list[0])
    obj[1].append(new_tag_list[0])
    obj[2].append(new_tag_list[0])

    return obj


def replace_attr(obj, param_list):

    for dic in param_list:
        for item in obj:
            item(dic['tag'], {'class': dic['old']})[0]['class'] = dic['new']

    return obj


def get_item_price(price_tag_obj):
    price = {'Price': None, 'SalePrice': None}
    if price_tag_obj('span', {'class': 'dcprice'}):
        price['Price'] = common_fn.get_integer(price_tag_obj('span', {'class': 'gpr_del'})[0].text)
        price['SalePrice'] = common_fn.get_integer(price_tag_obj('span', {'class': 'gpr_sale'})[0].text)
    else:
        price['Price'] = common_fn.get_integer(price_tag_obj('span', {'class': 'gpr_orig'})[0].text)
        price['SalePrice'] = None

    return price

if __name__ == "__main__":
    html = get_html('http://www.1300k.com/shop/best/best.html?f_bid=HD4001')
    soup = BeautifulSoup(html, 'html.parser')
    # item_list = soup.select('.gc_glst > li')
    # img = soup.select('.gds_img img')[0]['src']
    tmp = soup.select('.bst_rank .rank_bx2 li')
    new_tag2 = soup.new_tag('span', attrs={'class': 'gimg',
                                           'gimg': 'http://imgc.1300k.com/aaaaaib/goods/215024/59/215024596347.jpg?3'})
    tmp = insert_tag(tmp, [new_tag2])

    print(tmp)







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