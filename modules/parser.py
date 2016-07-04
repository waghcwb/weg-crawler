#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger    import Logger as log
from modules.helper    import Helper as helper
from modules.generator import Generator as generator
from bs4               import BeautifulSoup
from datetime          import datetime

import os
import html


class Parser(object):
	def __init__(self):
		super(Parser, self).__init__()


	@staticmethod
	def content(content, nid, catalog, link):
		if not content[0]:
			return 'Conteúdo vazio'

		document = BeautifulSoup(content[0].encode('utf-8'), 'html.parser')
		toRemove = ['comparison', 'bgdark', 'bglight', 'default', 'clr', 'novaJanela']
		imageBaseURL = 'news/'
		baseURL  = 'http://static.weg.net'

		for item in toRemove:
			if document.select('.{selector}'.format(selector=item)):
				for element in document.select('.{selector}'.format(selector=item)):
					index = element['class'].index(item)
					del element['class'][index]

		if document.select('img'):
			images = document.select('img')

			for image in images:
				filename = os.path.basename(image['src'].replace('http://www.weg.net/', ''))
				folder   = imageBaseURL + 'notice-{catalog}-'.format(catalog=catalog.upper()) + str(nid).zfill(4)
				path     = '{folder}/{filename}'.format(folder=folder, filename=filename)

				generator.setImage(image, nid, catalog)

				image.attrs['src'] = '{base}/{filename}'.format(base=baseURL, filename=path)

		if document.select('a[rel="image-galery-zoom"]'):
			for link in document.select('a[rel="image-galery-zoom"]'):
				filename = os.path.basename(link['href'].replace('http://www.weg.net/', ''))
				folder   = imageBaseURL + 'notice-{catalog}-'.format(catalog=catalog.upper()) + str(nid).zfill(4)
				path     = '{folder}/{filename}'.format(folder=folder, filename=filename)

				generator.setImage(link, nid, catalog)
				image.attrs['href'] = '{base}/{filename}'.format(base=baseURL, filename=path)

		if document.select('.center'):
			for center in document.select('.center'):
				center['class'] = 'text-center'

		if document.select('p'):
			paragraphs = document.select('p')

			for paragraph in paragraphs:
				for content in paragraph.contents:
					if content == '\xa0' or not content:
						paragraph.decompose()

		# if document.select('table'):
		# 	tables = document.select('table')
		# 	tablefilename = 'logs/weg/tables.list'

		# 	for table in tables:
		# 		toRemove = ['cellpadding', 'border', 'cellspacing', 'width', 'height']
		# 		responsive = document.new_tag('div')
		# 		responsive['class'] = 'table-responsive'
		# 		table.wrap(responsive)

		# 		table['class'].append('table table-bordered table-hover')

		# 		for item in toRemove:
		# 			del table[item]

		# 	if os.path.isfile(tablefilename):
		# 		content = helper.readFile(tablefilename)

		# 		if str(link['href']) not in str(content):
		# 			helper.createFile(tablefilename, '{link}\n'.format(link=link['href']))
		# 		else:
		# 			log.warning('Tabela já adicionada para a lista [{url}]'.format(url=link['href']))
		# 	else:
		# 		helper.createFile(tablefilename, '{link}\n'.format(link=link))
		# 		log.success('Log de tabelas criado.')
					

		if document.select('ul'):
			for ul in document.select('ul'):
				ul['class'] = 'xtt-list-style'

				for li in ul.select('> li'):
					span = document.new_tag('span')
					span.string = li.contents[0]
					li.string = ''
					li.append(span)

		return html.escape(str(document)).replace('&quot;', '""').replace('&gt;', '>').replace('&lt;', '<').strip()


	@staticmethod
	def title(title):
		return title[0].string if title and title[0] and title[0].string else ''


	@staticmethod
	def subtitle(subtitle):
		return subtitle[0].string if subtitle and subtitle[0] and subtitle[0].string else ''


	@staticmethod
	def banner(banner):
		return banner[0].get('src') if banner and banner[0] and banner[0].get('src') else 'empty'


	@staticmethod
	def date(publishDate):
		timestamp = publishDate[0].attrs['date-timestamp'] if publishDate and publishDate[0] and publishDate[0].attrs['date-timestamp'] else 0
		return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')


	@staticmethod
	def tags(tags):
		return ', '.join(tag.string for tag in tags) if tags else ''