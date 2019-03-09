import urllib.request
from bs4 import BeautifulSoup
import requests
import re

# def get_html(url):
#     response = urllib.request.urlopen(url)
#     return response.read()

# code below works well
r = requests.get("https://www.thecrag.com/climbing/ukraine/routes?page=1")
soup = BeautifulSoup(r.content, 'lxml')
table = soup.find_all('a')

addresses = []
for i in table:
    addresses.extend(re.findall("\/climbing.+\/route\/\d{2,}(?=\")", str(i)))


# k = i.get_text()
    # if k:
    #     result.append(k)

# print(soup.find_all("a"))
d = {}
pathes = []
for row, adres in zip(table, addresses):
    # print(i)

    z = (soup.find_all("a", {"href": adres}))
    # print(z)
    # each = soup.find("a", {"href": adres}).text
    # print(type(each))
    for i in z:
        way = i.attrs['title']
        path = way.split(" › ")
        path = [i.replace(u'\xa0', ' ') for i in path]
        # print(path)
        path.append(i.text)
        # print(i.text)
        pathes.append(path)


# print(pathes)

rez = []
difficulties = soup.find_all('span', {"class": re.compile("pull-right gb\d+")})



# print(rez)
for diff, pat in zip(difficulties, pathes):

    d[tuple(pat)] = diff.text

print(d)

result = []



# for loop to extract the relative path of each route:


# for i in table:
#     k = i.get_text()
#     if k:
#         result.append(k)
# print(result)
