from bs4 import BeautifulSoup
import requests
import re
import csv

from modules.exceptions import ParserException


def page_increment(num):
    num += 1
    return num


def url_processor(page):
    """
    Function for sending requests to certain url to get the web-page contents
    # >>> print(type(url_processor(1)))
    # <class 'bytes'>
    :param page: int - number of page in query parameter
    :return: bytes - web-page contents
    """
    address = "https://www.thecrag.com/climbing/world/routes"
    query = dict(sortby="popularity,desc", page=page)
    response = requests.get(address, params=query)
    return response.content


def format_title(bs_obj):
    """
    Function for getting the ascent title and its path in the readable
    representation
    :param bs_obj: bs4 - the table, that contains only the needed html tags
    :return: list
    """
    if bs_obj:
        splitted = bs_obj["title"].split("›")[1:]
        for el in range(len(splitted)):
            splitted[el] = splitted[el].replace("\xa0", '')
            splitted[el] = splitted[el].strip()

        return splitted + [bs_obj.text]
    else:
        return None


def get_lat_lon(bs_obj):
    """
    Function for getting latitude and longitude of each ascent and mountain
    :param bs_obj: Beautiful_soup object
    :return: list - list of coords

    """
    full_url = "https://www.thecrag.com" + bs_obj["href"]
    try:
        resp = requests.get(full_url)
        bs_obj = BeautifulSoup(resp.content, "lxml")
        rez = bs_obj.find("dl",
                          {"class": "areaInfo"}).text.strip()
        if "Lat/Long" not in rez:
            return None
        else:
            splited = rez.split()[1:]
            return ''.join(splited)
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
        raise ParserException(
            "The url contains an empty page.")
    for row in table:
        bs_obj = row.find("a", {"title": re.compile(".+")})
        title = format_title(bs_obj)
        if title:
            ascent_type = get_ascent_type(row)
            ascent_difficulty = get_ascent_difficulty(row)
            long_lat = get_lat_lon(bs_obj)
            write_to_file(title, ascent_type, ascent_difficulty[0],
                          ascent_difficulty[1], long_lat)


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

    with open("data.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        if location:
            writer.writerow(
                title + [style] + [difficulty] + [category] + [
                    location])


if __name__ == '__main__':
    from_page = 1
    to_page = 5900

    for page in range(from_page, to_page + 1):
        content = url_processor(page)
        try:
            rows = main_parser(content)
        except ParserException:
            with open("log.txt", "a") as f:
                f.write(content.url)
