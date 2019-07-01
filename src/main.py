import crawler_1300k
import time


def main():
    start = time.time()
    driver = crawler_1300k.get_driver()
    categories = crawler_1300k.get_category(driver)

    for category_key in categories.keys():
        html = crawler_1300k.get_html(driver, 'http://www.1300k.com/shop/best/best.html?f_bid=' + categories[category_key])
        data = crawler_1300k.crawl_1300k_best(html, category_key)
        crawler_1300k.insert_data(db_path="1300k_best.db", data=data)

    # html = crawler_1300k.get_html('http://www.1300k.com/shop/best/best.html?f_bid=41')
    # data = crawler_1300k.crawl_1300k_best(html)
    driver.quit()
    end_time = time.time() - start
    print(end_time)


if __name__ == "__main__":
    main()