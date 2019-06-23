import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def crawl_html(url, get_params=(), request_headers={}):
    response = requests.get(url)
    html = response.text
    print(html)


if __name__ == "__main__":
    # response = requests.get("http://www.1300k.com/shop/best/best.html?f_bid=HD4001")
    # print(response.encoding)
    # print(response.text)
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get('http://www.1300k.com/shop/best/best.html?f_bid=HD4001')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    brand_name = soup.select('.bst .a_bname')
    item_name = soup.select('.bst .a_gname')
    for item in brand_name:
        print(item.text)

    for item in item_name:
        print(item.text)
