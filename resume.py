#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: Morten Jakobsen © 2020

from LinkedInScraper.LinkedInScraper import Scraper

if __name__ == "__main__":

    s = Scraper("https://www.linkedin.com/jobs/view/1878186110/")
    s.get_page()
    s.set_title()
    s.set_company_contact()
    s.set_company_name()

    print(s.jobad)