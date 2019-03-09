import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import time

# def get_html(url):
#     response = urllib.request.urlopen(url)
#     return response.read()

# code below works well
def reader():

    # response = requests.get("https://www.thecrag.com/climbing/france/routes/page%3D1?page=1")
    i = 1
    response = requests.get("https://www.thecrag.com/climbing/ukraine/routes/?page=1")
    # return (response.url)
    # print(len(response.content))
    while 1:
    #
        if len(response.content) < 100000:
            break
        else:
            i += 1

            response = requests.get("https://www.thecrag.com/climbing/ukraine/routes/?page={}".format(str(i)))
            time.sleep(1)
            print(response.url)

#     starter_url = "https://www.thecrag.com/climbing/ukraine/routes?page=100"
    return response

print(reader())
# вызывать функцию с разными квери параметрами которые создаюся другой функцией
# def change_query():
#     i = 1
#     starter_q = "https://www.thecrag.com/climbing/ukraine/routes?page={}".format(str(i))
#     i += 1
#     return starter_q
# def parse(html):
#     soup = BeautifulSoup(html.content , 'lxml')
#     # print(soup)
#     table = soup.find_all('a')
#     # print(table)
#
#     addresses = []
#     for i in table:
#         addresses.extend(re.findall("\/climbing.+\/route\/\d{2,}(?=\")", str(i)))
#
#     pathes = []
#     for row, adres in zip(table, addresses):
#
#         z = (soup.find_all("a", {"href": adres}))
#
#         for i in z:
#             way = i.attrs['title']
#             path = way.split(" › ")
#             path = [i.replace(u'\xa0', ' ') for i in path]
#             path.append(i.text)
#
#             pathes.append(path)
#
#
#     difficulties = soup.find_all('span', {"class": re.compile("pull-right gb\d+")})
#
#
#
#     data = {}
#     for diff, pat in zip(difficulties, pathes):
#
#         data[tuple(pat)] = diff.text
#
#     print(data)
#
#
# change_query()
