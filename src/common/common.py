import requests


def get_integer(s):
    return int(''.join(filter(str.isdigit, s)))


def get_items_searchapi(keyword):
    response = requests.get('http://wapi.10x10.co.kr/search/getitemlist.asp?q={0}'.format(keyword))

    return response.text