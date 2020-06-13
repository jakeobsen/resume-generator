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
        mock_url = "https://raw.githubusercontent.com/jakeobsen/resume/master/LinkedInScraper/tests/mock/mock_ln.html"
        s = Scraper(mock_url)
        s.get_page()
        self.assertEqual(s.lnhtml[0], "<!DOCTYPE html")
        self.assertEqual(s.lnhtml[22], 'meta property="og:title" content="PostNord i Danmark hiring '
                                       'Python udvikler til PostNord Digital i København in København K,'
                                       ' Capital Region, Denmark | LinkedIn"/')

    def test_scraper_can_extract(self):
        s = Scraper("https://raw.githubusercontent.com/jakeobsen/resume/master/LinkedInScraper/tests/mock/mock_ln.html")

        s.set_title()
        self.assertEqual(s.jobad.position['title'], "")

        #s.set_company_contact()
        #self.assertEqual(s.jobad.company['att_contact']['name'], "")

        s.set_company_name()
        self.assertEqual(s.jobad.company['name'], "")

        s.get_page()

        s.set_title()
        self.assertEqual(s.jobad.position['title'], "Python udvikler til PostNord Digital i København")

        #s.set_company_contact()
        #self.assertEqual(s.jobad.company['att_contact']['name'], "")

        s.set_company_name()
        self.assertEqual(s.jobad.company['name'], "PostNord i Danmark")


if __name__ == '__main__':
    unittest.main()
