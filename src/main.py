import crawler_1300k
from match import MatchItems
from constant import URL_1300K_BEST
import time
import constant
from mysql_db import MysqlDatabase

def main():
    # db초기화
    # my_db = MysqlDatabase()
    # my_db.create_1300k_table()
    #
    # # 크롤링
    # start = time.time()
    # driver = crawler_1300k.get_driver()
    # categories = crawler_1300k.get_category(driver)
    #
    # for category_key in categories.keys():
    #     html = crawler_1300k.get_html(driver
    #                                   , '{url}?f_cno1={key}'.format(url=URL_1300K_BEST, key=categories[category_key]))
    #     data = crawler_1300k.crawl_1300k_best(html, driver, category_key)
    #
    #     my_db.insert_1300k_data(data)
    #     # crawler_1300k.insert_data(db_path=constant.DB_1300K_BEST_PATH, data=data)
    #
    # driver.quit()
    # end_time = time.time() - start
    # print(end_time)

    # 아이템 매칭

    match = MatchItems(img_similarity=0.9, text_similarity=0.85)
    match.run('전체')

if __name__ == "__main__":
    main()