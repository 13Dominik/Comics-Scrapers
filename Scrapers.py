#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime
import json
from abc import ABC, abstractmethod
from typing import List

import requests
import bs4

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class Scraper(ABC):

    def __init__(self, url: str, site: str, *args, **kwargs):
        self.url = url
        self.site = site
        self.last_date = None

    def __str__(self):
        return f"Scraper of site: {self.site}"

    def last_date_method(self) -> datetime.datetime:
        """
        Returns date from json file (if date and file exist)
        Returns date if date not in file but file exist
        Returns a date and create a file if file not exist
        :return: datetime.datetime
        """

        try:
            with open(os.path.join(THIS_DIR, "data_file.json"), mode='r') as json_file:
                try:
                    data = datetime.datetime.strptime(json.load(json_file)[self.site],
                                                      '%Y-%m-%d %H:%M:%S')
                    return data

                except:
                    return datetime.datetime(1970, 1, 1)
        except:
            with open(os.path.join(THIS_DIR, "data_file.json"), mode='a') as json_file:
                json.dump({}, json_file)
                json_file.close()

                return datetime.datetime(1970, 1, 1)

    def load_page(self) -> bs4.BeautifulSoup:
        """ Returns site response in bs4 format """

        res = requests.get(self.url)

        res.raise_for_status()
        return bs4.BeautifulSoup(res.text, 'html.parser')

    def save_image(self, url_and_filename: List[str]) -> None:
        """ Saves image from url to comics folder """

        res_jpg = requests.get(url_and_filename[0])
        res_jpg.raise_for_status()
        os.makedirs(os.path.join(THIS_DIR, 'comics'), exist_ok=True)
        open(os.path.join(THIS_DIR, f'comics/{url_and_filename[1]}'), "wb").write(res_jpg.content)

    def check_if_actuall(self) -> bool:
        """ Checks if new comics is available """

        return self.last_date >= self.get_last_image_date()

    def write_new_date(self) -> None:
        """ Writes date of last downloaded comics in data_file.json """

        with open(str(os.path.join(THIS_DIR, "data_file.json")), mode='r') as json_file:
            data = json.load(json_file)
            data[self.site] = str(self.get_last_image_date())
            json_file.close()
        with open(str(os.path.join(THIS_DIR, "data_file.json")), mode='w') as json_file:
            json.dump(data, json_file)
            json_file.close()

    @abstractmethod
    def find_last_image(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_last_image_date(self):
        raise NotImplementedError


class ScraperLefthandedtoons(Scraper):

    def __init__(self, *args, **kwargs) -> None:
        self.url = 'http://www.lefthandedtoons.com'
        self.site = "Lefthandedtoons"
        super().__init__(self.url, self.site, *args, **kwargs)

    # take a last_date from a data_file.json or create a empty file or add new key

    @property
    def last_date(self):
        return self.__last_date

    @last_date.setter
    def last_date(self, value):
        self.__last_date = self.last_date_method()

    def find_last_image(self) -> List[str]:
        """ Download the newest comics if its available """

        soup = self.load_page()
        url_to_down = soup.select('.comicimage')[0].get('src')

        filename = str(os.path.basename(url_to_down))

        return [url_to_down, filename]

    def get_last_image_date(self) -> datetime.datetime:
        """ Returns date of last comics from site """

        soup = self.load_page()
        header = soup.select('#comicwrap > div.comicnav.top > div')

        lst = header[0].text.split(" ")[-3:]
        lst[0] = lst[0][lst[0].find('\n') + 1:]

        return datetime.datetime.strptime(" ".join(lst), '%B %d, %Y')


class ScraperLunarbaboon(Scraper):

    def __init__(self, *args, **kwargs) -> None:
        self.url = 'http://www.lunarbaboon.com/'
        self.site = "Lunarbaboon"
        super().__init__(self.url, self.site, *args, **kwargs)

    @property
    def last_date(self):
        return self.__last_date

    # take a last_date from a data_file.json or create a empty file or add new key

    @last_date.setter
    def last_date(self, value):
        self.__last_date = self.last_date_method()

    def find_last_image(self) -> List[str]:
        """ Downloads new comics (if available)  """

        soup = self.load_page()

        txt_from_site = soup.select('.full-image-block')

        url_to_down = "http://www.lunarbaboon.com/" + str(txt_from_site[0])[
                                                      str(txt_from_site).find('/storage'):str(txt_from_site).find(
                                                          'SQUARESPACE_CACHEVERSION=') + 37]
        filename = str(url_to_down)[35:52]

        return [url_to_down, filename]

    def get_last_image_date(self) -> datetime.datetime:
        """ Returns date of last comics from site """

        soup = self.load_page()
        header = soup.select('.posted-on')
        data = header[0].getText()
        return datetime.datetime.strptime(data, " %A, %B %d, %Y at %I:%M%p")


def main() -> None:
    lb = ScraperLunarbaboon()
    if not lb.check_if_actuall():
        lb.save_image(lb.find_last_image())
        lb.write_new_date()
        print(f"last pic downloaded by: {lb}")

    lht = ScraperLefthandedtoons()
    if not lht.check_if_actuall():
        lht.save_image(lht.find_last_image())
        lht.write_new_date()
        print(f"last pic downloaded by: {lht}")


if __name__ == "__main__":
    main()
