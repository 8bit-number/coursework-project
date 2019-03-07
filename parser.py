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
# # (soup.find_all('a', class_='manga_img'))

# def parse(html):
#     soup = BeautifulSoup(html.content, features='lxml')
#
#     table = soup.find('table', class_="routetable facet-results")
# with open('prettified.html', 'w') as f:
#     f.write




# table = (soup.find_all('table', {"class": "routetable facet-results"}))
# table = (soup.string)
table = (soup.find_all('a', {"href": re.compile("/climbing/ukraine/crimea/route/\d+") }))
table2 = soup.find_all('span', {"class":"pull-right gb2"})
result = []

for i in table:
    # if i is not '':
    k = i.get_text()
    if k:
#     print(i.text.replace("\n\n\n", ''))
        result.append(k)
    # result = re.sub(r'\s+', ' ', text).strip()
print(result)
# result contains all names of routes


# for i in table2:
    # print(i.text)

    # f.write(table.())
# for i in table:
    # lst.append(i.text)

    # l = (i.text.replace('\n\n', '\n'))
    # print(l.replace('\n\n', '\n'))
    # if i.text:
    # print(i.prettify())
        # if i:
        #     f.write(i.text.strip())

    # with open("prettified.html") as data:
    #     readd = data.read()
    #     soup = BeautifulSoup(readd, features='lxml')
    #     print(soup.find_all("a"))
#         lst = []
#         fin = {}
#         al = re.findall("/climbing/ukraine/area/\w+\"|/climbing/ukraine/\w+\"", readd)
#         # print(al)
#         for link in al:
#             fin[(soup.find_all('a', {"href": link[:-1]})[0]).contents[0].strip()] =  "https://www.thecrag.com" + link[:-1]
#
#     return fin
#
# def create_file(file_names):
#
#     # file_names = parse(get_html("https://www.thecrag.com/climbing/ukraine"))
#     # for name in file_names:
#         # print(name)
#         # with open(name.replace("/", '_')+'.html', "w") as f:
#         #     resp = urllib.request.urlopen(file_names[name])
#         #     souup = BeautifulSoup(resp.read(), features='html.parser')
#             # f.write(souup.prettify())
#     new_names = parse("https://www.thecrag.com/climbing/ukraine/crimea")
#     print(new_names)

# def main():
#     parse(get_html("https://www.thecrag.com/climbing/ukraine/routes?page=1"))
# # https://www.thecrag.com/climbing/ukraine/routes?page=1
# main()
