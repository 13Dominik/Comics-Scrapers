#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import unittest
import os
from unittest import mock
from unittest.mock import patch, mock_open, PropertyMock

import requests

import Scrapers
from Scrapers import *


class TestScraperLefthandedtoons(unittest.TestCase):

    @patch('Scrapers.requests')
    def test_load_with_TimeoutError(self, mock_requests):
        fake_json_file = {
            'Lefthandedtoons': '2001-03-09 09:40:10'
        }
        fake = mock_open(read_data=json.dumps(fake_json_file))

        with patch('Scrapers.open', fake) as open_mock:
            mock_requests.get.side_effect = TimeoutError
            with self.assertRaises(TimeoutError):
                ScraperLefthandedtoons().load_page()


    @mock.patch('Scrapers.requests.models.Response')
    def test_get_site_date_find_last_image(self, mock_requests):
        fake_json_file = {
            'Lefthandedtoons': '2001-03-09 09:40:10'
        }
        fake = mock_open(read_data=json.dumps(fake_json_file))

        with open('data\\fake_Lefthandedtoons.html', 'r', encoding='utf-8') as html_file:
            with patch('Scrapers.open', fake) as open_mock:
                mock_requests.get.text = html_file.read()
                lht = ScraperLefthandedtoons()

                self.assertIsNotNone(lht.load_page())
                assert isinstance(lht.load_page(), bs4.BeautifulSoup)

                self.assertEqual(datetime.datetime(2018, 6, 27), ScraperLefthandedtoons().get_last_image_date())

                self.assertEqual(['http://www.lefthandedtoons.com/toons/drew_ariotheory.gif', 'drew_ariotheory.gif'],
                             lht.find_last_image())


    def test_last_date_method(self):
        fake_json_file = {
            'Lefthandedtoons': '2001-03-09 09:40:10'
        }
        fake_json_empty_file = {}

        fake = mock_open(read_data=json.dumps(fake_json_file))
        fake_empty = mock_open(read_data=json.dumps(fake_json_empty_file))

        with patch('Scrapers.open', fake) as open_mock:
            s = ScraperLefthandedtoons()
            self.assertEqual(datetime.datetime(2001, 3, 9, 9, 40, 10), s.last_date)
            self.assertEqual(datetime.datetime(2001, 3, 9, 9, 40, 10), s.last_date_method())
        with patch('Scrapers.open', fake_empty) as open_mock:
            s = ScraperLefthandedtoons()
            self.assertEqual(datetime.datetime(1970, 1, 1), s.last_date)
            self.assertEqual(datetime.datetime(1970, 1, 1), s.last_date_method())

    # mock property to test property and setter
    @mock.patch("Scrapers.ScraperLefthandedtoons.get_last_image_date", return_value=datetime.datetime(2070, 1, 1))
    def test_actuall_with_attr(self, mock_last_image_date):
        with mock.patch('Scrapers.ScraperLefthandedtoons.last_date', new_callable=PropertyMock) as mock_last_date:
            mock_last_date.return_value = datetime.datetime(1900, 1, 1)
            lht = ScraperLefthandedtoons()
            self.assertFalse(lht.check_if_actuall())


    @mock.patch("Scrapers.ScraperLefthandedtoons.last_date_method", return_value=datetime.datetime(1900, 1, 1))
    @mock.patch("Scrapers.ScraperLefthandedtoons.get_last_image_date", return_value=datetime.datetime(2070, 1, 1))
    def test_actuall_false(self, last_date_mock, image_last_date_mock):
        s = ScraperLefthandedtoons()
        self.assertFalse(s.check_if_actuall())


    @mock.patch("Scrapers.ScraperLefthandedtoons.last_date_method", return_value=datetime.datetime(2070, 1, 1))
    @mock.patch("Scrapers.ScraperLefthandedtoons.get_last_image_date", return_value=datetime.datetime(2070, 1, 1))
    def test_actuall_true(self, last_date_mock, image_last_date_mock):
        s = ScraperLefthandedtoons()
        self.assertTrue(s.check_if_actuall())


if __name__ == '__main__':
    unittest.main()