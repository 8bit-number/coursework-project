from bs4 import BeautifulSoup
import exceptions
import requests
import re
import csv


def page_increment(num):
    num += 1
    return num


def url_processor():
    """
    makes requests to the certain url-address
    :return:
    """
    address = "https://www.thecrag.com/climbing/world/routes"

    i = 0
    while 1:
        query = {"page": page_increment(i)}
        response = requests.get(address, params=query)
        try:
            main_parser(response.content)
            i += 1
        except exceptions.ParserException:
            with open("log.txt", "a") as f:
                f.write(response.url)
            break


def format_title(arg):
    if arg:
        splitted = arg["title"].split("›")[1:]
        for el in range(len(splitted)):
            splitted[el] = splitted[el].replace("\xa0", '')
            splitted[el] = splitted[el].strip()
        return splitted, splitted + [arg.text]
    else:
        return None


def get_lat_lon(arg):
    """
    Function for getting latitude and longitude of each ascent and mountain
    :param secondary_url: Beautiful_soup object
    :return:
    """
    full_url = "https://www.thecrag.com" + arg["href"]
    try:
        resp = requests.get(full_url)
        bs_obj = BeautifulSoup(resp.content, "lxml")
        rez = bs_obj.find("dl", {"class": "areaInfo"},
                          string=re.compile(
                              '\nLat/Long.+')).text.strip()[10:]
        return rez
    except:
        print(full_url)
        return "Unknown coords"


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
        arg = row.find("a", {"title": re.compile(".+")})
        if format_title(arg):
            write_to_file(format_title(row), get_ascent_type(row),
                          get_ascent_difficulty(row)[0],
                          get_ascent_difficulty(row)[1],
                          get_lat_lon(row))


def write_to_file(title, style, difficulty, category, location):
    """
    write all the data to the .csv file
    :param title: list
    :param style: str
    :param difficulty: str
    :param category: str
    :param location: str
    :return:
    """
    with open("locations_v11_2.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(
            title + [style] + [difficulty] + [category] + [location])


url_processor()
