#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.parser import Parser as parser
from datetime       import datetime
from bs4            import BeautifulSoup

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
		timestamp   = document.select('.noticia-detalhe .data')

		data = {
			'id':          nid,
			'title':       parser.title(title),
			'subtitle':    parser.subtitle(subtitle),
			'content':     parser.content(content, nid, catalog, link),
			'link':        link,
			'publishDate': parser.date(timestamp),
			'banner':      parser.banner(banner),
			'featured':    'false',
			'wegMagazine': '',
			'category':    category,
			'tags':        parser.tags(tags),
			'language':    language,
			'catalog':     catalog
		}

		return data