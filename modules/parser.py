#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger  import Logger as log
from bs4            import BeautifulSoup
from datetime       import datetime

import html
import os


class Parser(object):
	def __init__(self):
		super(Parser, self).__init__()


	@staticmethod
	def content(content):
		if not content[0]:
			return 'Conteúdo vazio'

		document = BeautifulSoup(content[0].encode('utf-8'), 'html.parser')
		toRemove = ['comparison', 'bgdark', 'bglight', 'default', 'clr', 'novaJanela']

		for item in toRemove:
			if document.select('.{selector}'.format(selector=item)):
				for element in document.select('.{selector}'.format(selector=item)):
					index = element['class'].index(item)
					del element['class'][index]

		if document.select('.texto'):
			for element in document.select('.texto'):
				index = element['class'].index('texto')
				element['class'][index] = 'post-content'

		if document.select('.center'):
			for center in document.select('.center'):
				center['class'] = 'text-center'

		if document.select('img'):
			images = document.select('img')

			for image in images:
				imagename = os.path.basename(image['src']).lower()
				print('Tratar imagem [{imagename}]'.format(imagename=imagename))

		if document.select('p'):
			paragraphs = document.select('p')

			for paragraph in paragraphs:
				for content in paragraph.contents:
					if content == '\xa0':
						paragraph.decompose()

		if document.select('table'):
			tables = document.select('table')
			tablefilename = 'logs/tables/tables.list'

			for table in tables:
				toRemove = ['cellpadding', 'border', 'cellspacing', 'width', 'height']
				responsive = document.new_tag('div')
				responsive['class'] = 'table-responsive'
				table.wrap(responsive)

				table['class'].append('table table-bordered table-hover')

				for item in toRemove:
					del table[item]

			if os.path.isfile(tablefilename):
				content = open(tablefilename, encoding='utf-8').read()

				if link not in content:
					with open(tablefilename, 'a+', encoding='utf-8') as file:
						file.write('{link}\n'.format(link=link))
				else:
					log.warning('Tabela já adicionada para a lista [{url}]'.format(url=link))
			else:
				with open(tablefilename, 'a+', encoding='utf-8') as file:
					file.write('{link}\n'.format(link=link))
					log.success('Log de tabelas criado.')

		if document.select('ul'):
			for ul in document.select('ul'):
				ul['class'] = 'xtt-list-style'

				for li in ul.select('> li'):
					span = document.new_tag('span')
					span.string = li.contents[0]
					li.string = ''
					li.append(span)

		return html.escape( str(document).strip() )


	@staticmethod
	def subtitle(subtitle):
		return subtitle[0].string if subtitle and subtitle[0] else 'Subtítulo vazio'


	@staticmethod
	def title(title):
		return title[0].string if title and title[0] else 'Título vazio'


	@staticmethod
	def banner(banner):
		return banner[0].get('src') if banner and banner[0] else 'empty'


	@staticmethod
	def date(publishDate):
		timestamp = publishDate[0].attrs['date-timestamp'] if publishDate and publishDate[0] else 0
		return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y')


	@staticmethod
	def tags(tags):
		return ', '.join(tag.string for tag in tags) if tags else ''