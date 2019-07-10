import requests
import textdistance
from constant import TEM_SEARCH_API

def get_integer(s):
    return int(''.join(filter(str.isdigit, s)))


def get_items_ten_api(keyword):
    response = requests.get(TEM_SEARCH_API+'?q={keyword}'.format(keyword=keyword))

    return response.text


def string_match(str1, str2):
    return textdistance.jaro.normalized_similarity(str1, str2)
