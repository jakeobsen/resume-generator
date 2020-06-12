#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: Morten Jakobsen © 2020

class JobAd:
    def __init__(self):
        self.company = {
            "name": None,
            "address": {
                "address_1": None,
                "address_2": None,
                "zipcode": None,
                "city": None,
                "country": None,
            },
            'main_contact': {
                'name': 'Primary contact',
                'email': None,
                'phone': None,
            },
            'att_contact': {
                'name': None,
                'email': None,
                'phone': None,
            }
        }
        self.position = {
            "title": None
        }

    def set_name(self, name):
        self.company['name'] = name

    def set_address(self,
                    address_1=None,
                    address_2=None,
                    zipcode=None,
                    city=None,
                    country=None,):
        self.company['address'] = {
                "address_1": address_1,
                "address_2": address_2,
                "zipcode": zipcode,
                "city": city,
                "country": country,
            }

    def set_contact(self,
                    name='Primary contact',
                    email=None,
                    phone=None,
                    who="main"):
        self.company[f'{who}_contact'] = {
                'name': name,
                'email': email,
                'phone': phone,
        }

    def set_title(self, title=""):
        self.position['title'] = title