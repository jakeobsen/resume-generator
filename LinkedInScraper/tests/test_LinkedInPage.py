#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: Morten Jakobsen © 2020

import unittest
from LinkedInScraper.LinkedInScraper import Scraper
from LinkedInScraper.JobAd import JobAd


class MyTestCase(unittest.TestCase):

    def test_scraper_init(self):
        url = "initial_value"
        s = Scraper(url)
        self.assertEqual(s.url, url)
        self.assertIsInstance(s.jobad, JobAd)
        self.assertIsInstance(s.lnhtml, list)
        self.assertEqual(len(s.lnhtml), 0)

    def test_scraper_can_scrape(self):
        s = Scraper("https://www.linkedin.com/jobs/view/1903515343/")

if __name__ == '__main__':
    unittest.main()
