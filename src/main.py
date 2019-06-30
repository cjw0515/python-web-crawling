import crawler_1300k
import time


def main():
    start = time.time()
    # html = crawler_1300k.get_html('http://www.1300k.com/shop/best/best.html?f_bid=HD4001')
    # data = crawler_1300k.crawl_1300k_best(html)
    # crawler_1300k.insert_data(db_path="test.db", data=data)
    print(crawler_1300k.get_category())
    end_time = time.time() - start

    print(end_time)


if __name__ == "__main__":
    main()