import requests


def get_integer(s):
    return int(''.join(filter(str.isdigit, s)))


def get_items_ten_api(keyword):
    response = requests.get('http://wapi.10x10.co.kr/search/getitemlist.asp?q={keyword}'.format(keyword=keyword))

    return response.text