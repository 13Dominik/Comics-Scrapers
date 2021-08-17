#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import unittest
import os
from unittest import mock
from unittest.mock import patch, mock_open, Mock

import requests

import Scrapers
from Scrapers import *

fake_json_file = {
    'Lunarbaboon': '2001-12-21 13:40:10'
}
fake = mock_open(read_data=json.dumps(fake_json_file))


# mocking whole class with fake_json_file as a fake data_file.json
@mock.patch('Scrapers.open', fake)
class TestScraperLunarbaboon(unittest.TestCase):

    def test_get_site_date_find_last_image(self):
        with open('data\\fake_Lunarbaboon.html', 'r', encoding='utf-8') as html_file:
            with patch("Scrapers.requests.get", return_value=Mock(text=html_file.read())):
                lb = ScraperLunarbaboon()

                self.assertIsNotNone(lb.load_page())
                assert isinstance(lb.load_page(), bs4.BeautifulSoup)
                self.assertEqual(datetime.datetime(2021, 8, 14, 10, 9), lb.get_last_image_date())
                self.assertEqual(['http://www.lunarbaboon.com/storage/comicartsmall.jpg?__SQUARESPACE_CACHEVERSION'
                                  '=1628950200716', 'comicartsmall.jpg'],
                                 lb.find_last_image())


if __name__ == '__main__':
    unittest.main()
