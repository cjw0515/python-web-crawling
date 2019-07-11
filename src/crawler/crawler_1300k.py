import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite_db
import common
import re
import logger
import traceback
from constant import URL_1300K_BEST
from urllib import parse


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', options=options)

    return driver


def get_html(driver, url, waiting=False):
    log = logger.logger('get_html')
    print("get html from %s" % url)
    log.info("get html from %s" % url)
    html = ''
    try:
        driver.get(url)
        if waiting:
            driver.implicitly_wait(waiting)
        html = driver.page_source
        # driver.quit()

    except Exception as e:
        print(traceback)
        log.error(e)

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
            "RegDate" DATETIME,
            "MatchedItem" TEXT
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


def crawl_1300k_best(html, category_name=None):

    log = logger.logger('crawl_1300k_best')
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.select('.gc_glst > li')

    # 같은 용도의 객체이나, 마크업이 다른것이 소수일 경우 메인로직에서 연산을 줄이기 위한 별도 처리과정 필요
    list_for_replace = [
        {'tag': 'span', 'old': 'gc_gpr_del', 'new': 'gpr_del'},
        {'tag': 'span', 'old': 'gc_gpr_sale', 'new': 'gpr_sale'},
        {'tag': 'span', 'old': 'gc_gpr_orig', 'new': 'gpr_orig'},
    ]

    best2to5 = replace_attr(soup.select('.bst_rank .rank_bx2 li'), list_for_replace)
    best1 = replace_attr(soup.select('.bst_rank .rank_bx1'), list_for_replace)
    # best1 상품 태그 삽입
    for item in best1:
        new_tag = soup.new_tag('span', attrs={"class": "ico_rank"})
        new_tag.string = "1"
        item.append(new_tag)
        item.append(soup.new_tag('span', attrs={'class': 'gimg', 'gimg': item('img')[0].attrs['src']}))
    # best2~5상품 태그 삽입
    for item in best2to5:
        item.append(soup.new_tag('span', attrs={'class': 'gimg', 'gimg': item('img')[0].attrs['src']}))

    item_list = item_list + best2to5
    item_list = item_list + best1

    item_arr = []

    for item in item_list:
        try:
            category = category_name
            rank = item('span', {'class': 'ico_rank'})[0].text
            image_URL = item('span', {'class': 'gimg'})[0].attrs['gimg']
            url = parse.urlparse(item.find('a', href=re.compile('goodsDetail.html?')).attrs['href'])
            item_code = parse.parse_qs(url.query)['f_goodsno'][0]
            brand = item('a', {'class': 'a_bname'})[0].text
            item_name = item('a', {'class': 'a_gname'})[0].text
            tmp_price_dic = get_item_price(item('span', {'class': 'gprice'})[0])
            price = tmp_price_dic['Price']
            sale_price = tmp_price_dic['SalePrice']
            num_of_review = None
            num_of_like = None
    ######################################
            # item_detail_url = 'http://www.1300k.com/shop/goodsDetail.html?f_goodsno=' + item_code
            # tmp_html = get_html(item_detail_url)
            #
            # soup = BeautifulSoup(tmp_html, 'html.parser')
            # num_of_like = common.get_integer(soup.select("#idGoodsFavorCnt")[0].text)
            # num_of_review = common.get_integer(soup.select("#gdt_nav_desc .txt_ps")[0]('em')[0].text)
    ######################################

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
        except Exception as e:
            log.error(e)
            traceback.print_exc()
            pass

    return item_arr


def get_category(driver):
    html = get_html(driver, URL_1300K_BEST)
    soup = BeautifulSoup(html, 'html.parser')

    category_dic = {}

    for item in soup.select('.bst .gc_gnb_cate a'):
        url = item.attrs['href']

        if re.search("shop/best/best.html\?f_cno1=", url):
            url_obj = parse.urlparse(url)
            category_code = parse.parse_qs(url_obj.query)['f_cno1'][0]
            category_name = item.text
            category_dic[category_name] = category_code

    category_dic['전체'] = 'HD4001'

    return category_dic


def insert_tag(obj, new_tag_list):
    idx = 0

    for item in obj:
        # print(tag)
        item.append(new_tag_list[idx])
        idx = idx + 1

    return obj


def replace_attr(obj, param_list):
    #
    # list_for_replace = [
    #     {'tag': 'span', 'old': 'gc_gpr_del', 'new': 'gpr_del'},
    #     {'tag': 'span', 'old': 'gc_gpr_sale', 'new': 'gpr_sale'}
    # ]
    #
    for dic in param_list:
        for item in obj:
            if len(item(dic['tag'], {'class': dic['old']})) > 0:
                item(dic['tag'], {'class': dic['old']})[0]['class'] = dic['new']

    return obj


def get_item_price(price_tag_obj):
    price = {'Price': None, 'SalePrice': None}
    if price_tag_obj('span', {'class': 'dcprice'}):
        price['Price'] = common.get_integer(price_tag_obj('span', {'class': 'gpr_del'})[0].text)
        price['SalePrice'] = common.get_integer(price_tag_obj('span', {'class': 'gpr_sale'})[0].text)
    else:
        price['Price'] = common.get_integer(price_tag_obj('span', {'class': 'gpr_orig'})[0].text)
        price['SalePrice'] = None

    return price


if __name__ == "__main__":
    print('crawler')

