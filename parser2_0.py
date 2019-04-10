from bs4 import BeautifulSoup
import requests
import re
import time
import csv


def is_empty(url):
    """
    checks whether the web page that is behind a specific address is empty
    :param url: str - url address
    :return: bool
    """
    resp = requests.get(url)
    return len(resp.content) < 100000


def url_processor():
    """
    makes requests to the certain url-address
    :return:
    """
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
            if is_empty(address):
                break

            else:
                address = re.search(".+=", address).group(0) + '{}'.format(
                    str(i))
                response = requests.get(address)
                time.sleep(3)
                main_parser(response)
                i += 1


def get_ascent_title(bs_obj):
    """
    gets the ascent title
    :param bs_obj: BeautifulSoup object
    :return: str
    """
    rez = bs_obj.find("a", {"title": re.compile(".+")})
    if rez:
        return rez["title"]


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


def get_ascent_difficulty(bs_obj):
    """
    gets the ascent difficulty: Considering the fact, that some countries have
    their own grading, this data is important
    :param bs_obj:  BeautifulSoup object
    :return: str
    """
    rez = bs_obj.find('span', {"class": re.compile("pull-right gb\d+")})
    if rez:
        return rez.text


def main_parser(html):
    """
    function to process all needed data call other minor functions
    :param html: html contents of the web-site
    :return: None
    """
    soup = BeautifulSoup(html.content, 'lxml')
    table = soup.find_all('tr')
    for row in table:
        if get_ascent_title(row):
            write_to_file(get_ascent_title(row), get_ascent_type(row),
                          get_ascent_difficulty(row))

    print("the data was written to the file successfully!")


def write_to_file(title, style, difficulty):
    """
    write all the data to the .csv file
    :param title: str
    :param style: str
    :param difficulty: str
    :return:
    """
    with open("test_first_page.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([title] + [style] + [difficulty])


main_parser(
    requests.get("https://www.thecrag.com/climbing/australia/routes?page=1"))
