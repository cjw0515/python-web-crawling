import htmlcrawler
import sqlite_db
import bestitem_1300k


def main():
    html = htmlcrawler.get_html('http://www.1300k.com/shop/best/best.html?f_bid=HD4001')
    data = htmlcrawler.crawl_1300k_best(html)
    print(data)
    # htmlcrawler.insert_data(db_path="test.db", data=data)


if __name__ == "__main__":
    main()