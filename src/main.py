import htmlcrawler
import time


def main():
    start = time.time()
    html = htmlcrawler.get_html('http://www.1300k.com/shop/best/best.html?f_bid=HD4001')
    data = htmlcrawler.crawl_1300k_best(html)
    htmlcrawler.insert_data(db_path="test.db", data=data)
    end_time = time.time() - start

    print(end_time)

if __name__ == "__main__":
    main()