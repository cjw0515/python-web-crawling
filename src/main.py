import sys
import htmlcrawler

# sys.path
def main():
    get_params = (('f_bid', 'HD4001'), ('a', 'b'))
    htmlcrawler.crawl_html("http://www.1300k.com/shop/best/best.html?f_bid=HD4001")
    # sys.path.append("D:/python-workspace/python-web-crawling/src/crawler")
    # print(sys.path)


if __name__ == "__main__":
    main()