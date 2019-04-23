from bs4 import BeautifulSoup
import modules.exceptions
import requests
import re
import time
import csv


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
            # print(response.)
            time.sleep(3)
            try:
                main_parser(response.content)
                i += 1
            except modules.exceptions.ParserException:
                with open("log.txt", "a") as f:
                    f.write(response.url)
                break


def get_ascent_title(bs_obj):
    """
    gets the ascent title
    :param bs_obj: BeautifulSoup object
    :return: str
    """
    rez = bs_obj.find("a", {"title": re.compile(".+")})
    if rez:
        splitted = rez["title"].split("›")[1:]
        for el in range(len(splitted)):
            splitted[el] = splitted[el].replace("\xa0", '')
            splitted[el] = splitted[el].strip()
        return splitted
    else:
        return None


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
    rez = bs_obj.find('span', {"class": re.compile("pull-right gb\d+")})
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
        raise modules.exceptions.ParserException(
            "The url contains an empty page.")

    for row in table:
        if get_ascent_title(row):
            write_to_file(get_ascent_title(row), get_ascent_type(row),
                          get_ascent_difficulty(row)[0],
                          get_ascent_difficulty(row)[1])


def write_to_file(title, style, difficulty, category):
    """
    write all the data to the .csv file
    :param title: str
    :param style: str
    :param difficulty: str
    :param category: str
    :return:
    """
    with open("final_file_with_all_data.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(title + [style] + [difficulty] + [category])


url_processor()
