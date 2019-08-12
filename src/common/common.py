import requests
import textdistance
import time
import sys
import os
from constant import TEM_SEARCH_API


def get_integer(s):
    return int(''.join(filter(str.isdigit, s)))


def get_items_ten_api(keyword):
    response = requests.get(TEM_SEARCH_API+'?q={keyword}'.format(keyword=keyword))

    return response.text


class Waiting:
    def __init__(self):
        self.done = False

    def print_waiting(self):
        animation = "|/-"

        i = 0
        while not self.done:
            time.sleep(0.1)
            sys.stdout.write("\r" + animation[i % len(animation)])
            i += 1
            sys.stdout.flush()


def string_match(str1, str2):
    return textdistance.jaro.normalized_similarity(str1, str2)


def remove_all_files(path):
    if os.path.exists(path):
        for file in os.scandir(path):
            os.remove(file.path)

