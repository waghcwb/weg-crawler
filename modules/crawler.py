#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests


class Crawler(object):
	def __init__(self):
		super(Crawler, self).__init__()


	@staticmethod
	def request(url, parser='html.parser'):
		return BeautifulSoup(requests.get(url).text, parser)