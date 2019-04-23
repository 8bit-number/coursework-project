from bs4 import BeautifulSoup
import exceptions
import requests
import urllib.request
import re
import time
import csv

NAME = list()
COORDS = list()


def page_increment(num):
    num += 1
    return num


def url_processor():
    """
    makes requests to the certain url-address
    :return:
    """
    places_list = ["https://www.thecrag.com/climbing/australia/routes",
                   "https://www.thecrag.com/climbing/new-zealand/routes",
                   "https://www.thecrag.com/climbing/pacific-islands/routes",
                   "https://www.thecrag.com/climbing/north-america/routes",
                   "https://www.thecrag.com/climbing/central-america/routes",
                   "https://www.thecrag.com/climbing/south-america/routes",
                   "https://www.thecrag.com/climbing/europe/routes",
                   "https://www.thecrag.com/climbing/africa/routes",
                   "https://www.thecrag.com/climbing/middle-east/routes",
                   "https://www.thecrag.com/climbing/asia/routes"
                   ]

    for address in places_list:
        i = 0
        while 1:
            query = {"page": page_increment(i)}
            response = requests.get(address, params=query)
            # time.sleep(3)
            try:
                main_parser(response.content)
                i += 1
            except exceptions.ParserException:
                with open("log.txt", "a") as f:
                    f.write(response.url)
                break


def format_title(bs_obj):
    rez = bs_obj.find("a", {"title": re.compile(".+")})
    if rez:
        # print(rez["title"])
        splitted = rez["title"].split("›")[1:]
        for el in range(len(splitted)):
            splitted[el] = splitted[el].replace("\xa0", '')
            splitted[el] = splitted[el].strip()

        return splitted, splitted + [rez.text]
    else:
        return None


# def get_ascent_title(rez):
# """
# gets the ascent title
# :param bs_obj: BeautifulSoup object
# :return: str
# """
#
#     NAME.append(splitted)
#     return splitted


def get_lat_lon(bs_obj):
    """
    Function for getting latitude and longitude of each ascent and mountain
    :param secondary_url: Beautiful_soup object
    :return:
    """
    secondary_url = bs_obj.find("a", {"title": re.compile(".+")})

    full_url = "https://www.thecrag.com" + secondary_url["href"]
    resp = urllib.request.urlopen(full_url)
    bs_obj = BeautifulSoup(resp, "lxml")
    rez = bs_obj.find("dl", {"class": "areaInfo"},
                      string=re.compile(
                          '\nLat/Long.+')).text.strip()[10:]
    COORDS.append(rez)
    return rez

    # else:
    #     return "Unknown coords"


# print(get_lat_lon("/climbing/switzerland/denti-della-vecchia/route/1868627349"))
def check_eq(bs_obj):
    # secondary_url = bs_obj.find("a", {"title": re.compile(".+")})
    x = format_title(bs_obj)
    if x[0] in NAME:
        # title, coord
        return x[1], COORDS[-1]
    else:
        return x[1], get_lat_lon(bs_obj)


def get_ascent_type(bs_obj):
    """
    gets the ascent style: Boulder, Mixed, Trad
    it will be useful for future difficulties classification and their representation
    :param bs_obj: BeautifulSoup object
    :return: str
    """
    rez = bs_obj.find("span", {"class": re.compile("tags .+")})
    if rez:
        return rez.text
    return "Unknown"


def get_ascent_difficulty(bs_obj):
    """
    gets the ascent difficulty: Considering the fact, that some countries have
    their own grading, this data is important
    :param bs_obj:  BeautifulSoup object
    :return: str
    """
    rez = bs_obj.find('span',
                      {"class": re.compile("pull-right gb\d+")})
    category = bs_obj.find("span")["class"][1]
    if rez:
        return rez.text, category
    return "Unknown", "Unknown"


def main_parser(html):
    """
    function to process all needed data call other minor functions
    :param html: html contents of the web-site
    :return: None
    """
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('tr')

    if len(table) == 1:
        raise exceptions.ParserException(
            "The url contains an empty page.")

    for row in table:
        # print(get_lat_lon(row))
        # arg = row.find("a", {"title": re.compile(".+")})

        if format_title(row):
            x = check_eq(row)
            write_to_file(x[0], get_ascent_type(row),
                          get_ascent_difficulty(row)[0],
                          get_ascent_difficulty(row)[1],
                          x[1])


def write_to_file(title, style, difficulty, category, location):
    """
    write all the data to the .csv file
    :param title: str
    :param style: str
    :param difficulty: str
    :param category: str
    :return:
    """

    with open("locs_tesst.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(
            title + [style] + [difficulty] + [category] + [location])


url_processor()

# from file_contents import data
# main_parser(data)
# print(get_lat_lon("/climbing/switzerland/denti-della-vecchia/route/1868627349"))