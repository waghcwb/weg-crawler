#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger  import Logger as log
from bs4            import BeautifulSoup
from datetime       import datetime

import html


class Parser(object):
	def __init__(self):
		super(Parser, self).__init__()


	@staticmethod
	def content(content):
		if content[0]:
			print( content[0].encode("utf-8") )
		else:
			return 'Conteúdo vazio'
		# return html.escape( str(content).strip() ).encode('utf-8')
		# str(content[0]) if content[0] else ''


	@staticmethod
	def subtitle(subtitle):
		return subtitle[0].string if subtitle[0] else 'Subtítulo vazio'


	@staticmethod
	def title(title):
		return title[0].string if title[0] else 'Título vazio'


	@staticmethod
	def banner(banner):
		return banner[0].get('src') if banner[0] else 'empty'


	@staticmethod
	def date(publishDate):
		timestamp = publishDate[0].attrs['date-timestamp'] if publishDate[0] else 0
		return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')


	@staticmethod
	def tags(tags):
		return ', '.join(tag.string for tag in tags) if tags else ''