#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

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
		banner      = document.select('.imagem-corpo-noticia img')[0].get('src') if document.select('.imagem-corpo-noticia img') else 'empty'
		content     = html.escape(str(document.select('.coluna5 .texto')[0])).encode('ascii', 'xmlcharrefreplace').decode()
		timestamp   = document.select('.noticia-detalhe .data')[0].attrs['date-timestamp']
		publishDate = datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')