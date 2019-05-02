from bs4 import BeautifulSoup
import exceptions
import requests
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
    address = "https://www.thecrag.com/climbing/world/routes"
    # places_list = ["https://www.thecrag.com/climbing/europe/routes",
    #                "https://www.thecrag.com/climbing/australia/routes",
    #                "https://www.thecrag.com/climbing/new-zealand/routes",
    #                "https://www.thecrag.com/climbing/pacific-islands/routes",
    #                "https://www.thecrag.com/climbing/north-america/routes",
    #                "https://www.thecrag.com/climbing/central-america/routes",
    #                "https://www.thecrag.com/climbing/south-america/routes",
    #                "https://www.thecrag.com/climbing/africa/routes",
    #                "https://www.thecrag.com/climbing/middle-east/routes",
    #                "https://www.thecrag.com/climbing/asia/routes"
    #                ]

    # for address in places_list:
    i = 0
    while 1:
        query = {"page": page_increment(i)}
        response = requests.get(address, params=query)
        # response = requests.get("https://www.thecrag.com/climbing/australia/grampians/dreamtime-wall/routes")
        # time.sleep(3)
        try:
            main_parser(response.content)
            i += 1
        except exceptions.ParserException:
            with open("log.txt", "a") as f:
                f.write(response.url)
            break


def format_title(arg):
    # rez = bs_obj.find("a", {"title": re.compile(".+")})
    if arg:
        # print(rez["title"])
        splitted = arg["title"].split("›")[1:]
        for el in range(len(splitted)):
            splitted[el] = splitted[el].replace("\xa0", '')
            splitted[el] = splitted[el].strip()
        NAME.append(splitted)
        # print(s)
        return splitted, splitted + [arg.text]

    else:
        # return "none"
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

def get_lat_lon(arg):
    """
    Function for getting latitude and longitude of each ascent and mountain
    :param secondary_url: Beautiful_soup object
    :return:
    """
    # secondary_url = bs_obj.find("a", {"title": re.compile(".+")})

    full_url = "https://www.thecrag.com" + arg["href"]
    try:
        resp = requests.get(full_url)
        bs_obj = BeautifulSoup(resp.content, "lxml")
        rez = bs_obj.find("dl", {"class": "areaInfo"},
                          string=re.compile(
                              '\nLat/Long.+')).text.strip()[10:]
        COORDS.append(rez)
        return rez
    except:
        print(full_url)
        return "Unknown coords"


def check_eq(arg):
    # secondary_url = bs_obj.find("a", {"title": re.compile(".+")})
    x = format_title(arg)
    y = get_lat_lon(arg)
    # # if y:
    return x[1], y
    # print(x[0][-2], NAME[-2][-2])
    # print(NAME[-1][-2])
    # print(COORDS)
    # if x[0][-2] == NAME[-1][-2]:
    #     # title, coord
    #
    #     # return x[1], COORDS[-1]
    #
    #     return x[1], "if"
    # else:
    #     return x[1], "else"
    # return x[1], y


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
        arg = row.find("a", {"title": re.compile(".+")})

        if format_title(arg):
            x = check_eq(arg)
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

    with open("locations_v11_2.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(
            title + [style] + [difficulty] + [category] + [location])


url_processor()
