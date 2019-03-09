from bs4 import BeautifulSoup
import requests
import re
import time


def reader():


    i = 1
    response = requests.get("https://www.thecrag.com/climbing/ukraine/routes/?page=1")

    while 1:
    #
        if len(response.content) < 100000:
            break
        else:
            i += 1

            response = requests.get("https://www.thecrag.com/climbing/ukraine/routes/?page={}".format(str(i)))
            time.sleep(1)
            print(response.url)

    return response


def parse(html):

    soup = BeautifulSoup(html.content , 'lxml')
    table = soup.find_all('a')

    addresses = []
    for i in table:
        addresses.extend(re.findall("\/climbing.+\/route\/\d{2,}(?=\")", str(i)))

    pathes = []
    for row, adres in zip(table, addresses):

        z = (soup.find_all("a", {"href": adres}))

        for i in z:
            way = i.attrs['title']
            path = way.split(" › ")
            path = [i.replace(u'\xa0', ' ') for i in path]
            path.append(i.text)
            pathes.append(path)


    difficulties = soup.find_all('span', {"class": re.compile("pull-right gb\d+")})



    data = {}
    for diff, pat in zip(difficulties, pathes):
        data[tuple(pat)] = diff.text

    print(data)


