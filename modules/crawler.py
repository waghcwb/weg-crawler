#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from bs4      import BeautifulSoup

import requests


class Crawler(object):
	def __init__(self):
		super(Crawler, self).__init__()


	@staticmethod
	def getData(nid, category, language, catalog, link, parser='html.parser'):
		html = BeautifulSoup(requests.get(link).text, parser)
		return Crawler.parseData(html, nid, category, language, catalog, link)

	@staticmethod
	def parseData(document, nid, category, language, catalog, link):
		title       = document.select('.noticia-titulo h1')
		subtitle    = document.select('.noticia-titulo h2')
		tags        = document.select('.tags a')
		banner      = document.select('.imagem-corpo-noticia img')
		content     = document.select('.coluna5 .texto')
		timestamp   = document.select('.noticia-detalhe .data')[0].attrs['date-timestamp']
		publishDate = datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')

		data = {
			'id':          nid,
			'title':       str(title[0].contents[0]) if title[0].contents else '',
			'subtitle':    str(subtitle[0].contents[0]) if subtitle[0].contents else '',
			'content':     str(content[0].contents[0]) if content[0].contents else '',
			'link':        link,
			'publishDate': publishDate,
			'banner':      banner[0].get('src') if banner[0] else 'empty',
			'featured':    False,
			'wegMagazine': '',
			'category':    category,
			'tags':        ', '.join(str(x.contents[0]) for x in tags),
			'language':    language,
			'catalog':     catalog
		}

		print(data)

		return data