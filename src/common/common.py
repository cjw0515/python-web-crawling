import requests
from constant import TEM_SEARCH_API
import constant
import os


def get_integer(s):
    return int(''.join(filter(str.isdigit, s)))


def get_items_ten_api(keyword):
    response = requests.get(TEM_SEARCH_API+'?q={keyword}'.format(keyword=keyword))

    return response.text


if __name__ == "__main__":
    file_list1 = os.listdir(constant.IMG_1300k_DIR)
    file_list2 = os.listdir(constant.IMG_10x10_DIR)
    print(file_list1)
    print(file_list2)