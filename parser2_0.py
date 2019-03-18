from bs4 import BeautifulSoup
import requests
import re
import time
import csv


def if_empty(url):
    resp = requests.get(url)
    return len(resp.content) < 100000


def reader():
    
    places_list = ["https://www.thecrag.com/climbing/australia/routes?page=1",
                   "https://www.thecrag.com/climbing/new-zealand/routes?page=1",
                   "https://www.thecrag.com/climbing/pacific-islands/routes?page=1",
                   "https://www.thecrag.com/climbing/north-america/routes?page=1",
                   "https://www.thecrag.com/climbing/central-america/routes?page=1",
                   "https://www.thecrag.com/climbing/south-america/routes?page=1",
                   "https://www.thecrag.com/climbing/europe/routes?page=1",
                   "https://www.thecrag.com/climbing/africa/routes?page=1",
                   "https://www.thecrag.com/climbing/middle-east/routes?page=1",
                   "https://www.thecrag.com/climbing/asia/routes?page=1"
                   ]

    for address in places_list:
        i = 1
        while 1:
            if if_empty(address):
                print(address + " is empty")
                break

            else:
                address = re.search(".+=", address).group(0) + '{}'.format(str(i))
                response = requests.get(address)
                time.sleep(3)
                parse(response)
                i += 1


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

    with open("all_locations.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for diff, pat in zip(difficulties, pathes):
            writer.writerow([diff.text] + pat)


reader()

