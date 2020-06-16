#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: Morten Jakobsen © 2020

import contextlib
import json
import urllib.parse
import urllib.request as request

class Scraper:

    def __init__(self, url) -> None:
        """
        Scraper constructor - Initialize object
        :param url:
        """
        self.url = url
        self.lnhtml = []

    def get_page(self) -> None:
        """ Fetch page from linkedin and store in object """
        request_a = request.Request(url=self.url)
        with contextlib.closing(request.urlopen(request_a)) as response:
            data = response.read()
        self.lnhtml = data.decode().split("><")

    def search_pattern(self, pattern) -> str:
        """
        Search for pattern in fetched page

        :param pattern: pattern to look for
        :return: returns the found result
        """
        result = ""
        for line in self.lnhtml:
            if pattern in line:
                result = line.split(">")[1].split("<")[0]
                break
        return result

    @staticmethod
    def lookup_cvr(string="", language="dk") -> dict:
        """
        Search danish CVR registry for a company info and their details

        :param string: Search string
        :param language: ISO code of country, default: dk
        :return: dict with results from cvr - empty dict on error
        """
        request_a = request.Request(headers={'User-Agent': 'Job Database'},
            url='http://cvrapi.dk/api?search=%s&country=%s' % (urllib.parse.quote(string),language))
        try:
            with contextlib.closing(request.urlopen(request_a)) as response:
                data = json.loads(response.read())
        except Exception as e:
            data = {}
        return data

if __name__ == "__main__":
    import argparse
    from datetime import datetime
    from time import sleep
    from os import remove, rename, getcwd
    from os.path import expanduser
    from subprocess import run

    parser = argparse.ArgumentParser(description="Resume Builder")
    parser.add_argument('texfile', metavar='T', type=str, help='LaTeX template file')
    parser.add_argument('url', metavar='U', type=str, nargs='+', help='LinkedIn URL')
    args = parser.parse_args()

    for url in args.url:
        texvars = {
            "companyName": "",
            "companyAddress": "",
            "companyCityZip": "",
            "companyATT": "",
            "positionName": "",
            "adLocation": "LinkedIn",
            "firstValue": "structured",
            "secondValue": "focused",
            "thirdValue": "proactive",
            "jobAdLink": url,
        }

        s = Scraper(url)
        s.get_page()

        texvars['companyName'] = s.search_pattern("public_jobs_topcard_org_name")
        cvr_data = Scraper.lookup_cvr(string=texvars['companyName'])

        # Sometimes the ATT person does not show in linkedins results, so we need to rescrape a few times to get it
        n = 0
        while texvars['companyATT'] == '':
            texvars['companyATT'] = s.search_pattern("profile-result-card__title")
            n += 1
            if n > 5:
                break
            sleep(1)
            s.get_page()
            print(f"[{n}/5] Rescraping for att contact name")

        # Update variables
        texvars['companyATT'] = "Hiring manager" if texvars['companyATT'] == "" else texvars['companyATT']
        texvars['positionName'] = s.search_pattern("topcard__title")
        texvars['companyName'] = cvr_data['name'] if texvars['companyName'] == "" else texvars['companyName']
        texvars['companyAddress'] = cvr_data['address']
        texvars['companyCityZip'] = f"{cvr_data['zipcode']} {cvr_data['city']}"

        # Write latex file with variables we've collected
        file = ""
        for var, val in texvars.items():
            val = input(f"{var}: ") if val == "" else val
            file += '\\newcommand{{\\' + var + '}}{' + val + '}\n'
        del(var, val)

        file += "{}{}{}".format("\input{", args.texfile, "}")
        with open('.latex_application_temp.tex', 'w')as fw:
            fw.write(file)

        # Prepare a filename
        date = datetime.now()
        filename = f"{expanduser('~/Desktop/')}{date.year}-{date.month}-{date.day}_{texvars['companyName'].replace(' ', '_').replace('/','')}.pdf"

        # generate outout
        run("xelatex .latex_application_temp.tex", shell=True, check=True)
        remove(".latex_application_temp.aux")
        remove(".latex_application_temp.log")
        remove(".latex_application_temp.tex")
        rename(f'.latex_application_temp.pdf', f'{filename}')
        run(f'open {filename}', shell=True, check=True)