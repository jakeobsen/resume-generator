#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: Morten Jakobsen © 2020

import urllib.parse
import urllib.request as request
import json
import contextlib

from LinkedInScraper.JobAd import JobAd


class Scraper:

    def __init__(self, url):
        self.url = url
        self.jobad = JobAd()
        self.lnhtml = []

    def get_page(self):
        request_a = request.Request(url=self.url)
        with contextlib.closing(request.urlopen(request_a)) as response:
            data = response.read()
        self.lnhtml = data.decode().split("><")

    def search_pattern(self, pattern):
        result = ""
        for line in self.lnhtml:
            if pattern in line:
                result = line.split(">")[1].split("<")[0]
                break
        return result

    def set_title(self):
        result = self.search_pattern("topcard__title")
        print(result)
        self.jobad.set_title()

    def set_company_name(self):
        result = self.search_pattern("public_jobs_topcard_org_name")
        print(result)
        self.jobad.set_name(result)

    def set_company_contact(self):
        result = self.search_pattern("profile-result-card__title")
        print(result)
        self.jobad.set_contact(name=result, who="att")

    def get_cvr_info(cvr, country='dk'):
        request_a = request.Request(
            url='http://cvrapi.dk/api?search=%s&country=%s' % (urllib.parse.quote(cvr), country),
            headers={'User-Agent': 'Job Database'})
        with contextlib.closing(request.urlopen(request_a)) as response:
            return json.loads(response.read())
