import requests
import json
from bs4 import BeautifulSoup


# 커스텀 헤더
request_header = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
    'Referer': 'http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=20170714'
}
# get 인자
# dict, key,value형식의 tuple 두가지로 지정할 수 있다.
# 웹에서는 동일키를 지원해주기 때문에 다수의 인자값 지정이 가능한 tuple타입으로 사용하는게 맞다

getParams = (('k1', 'v1'), ('k1', 'v1'), ('k1', 'v1'))
getParams2 = dict([('k1', 'v1'), ('k1', 'v3'), ('k2', 'v2')])


# get 요청
response = requests.get('http://httpbin.org/get', params=getParams)
# print(response.json())
# print(response.text)
# print(response.headers['content-type'])

# JSON POST 요청
jsonData = {'k1': 'v2', 'k2': [1,2,3], 'name': 'rednooby'}

jsonString = json.dumps(jsonData)
response = requests.post('http://httpbin.org/post', data=jsonString)

print(response.text)

# response = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
# response = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn', headers=request_header, params=getParams)
response = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn', params=getParams)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
result = soup.select('div[class=tit3]')

movies = list()

for tag in result:
    movies.append(tag.text.strip())

# print(movies[0])

# for item in movies:
#     print(item)

print(__name__)