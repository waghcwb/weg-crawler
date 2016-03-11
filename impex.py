#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log
from sys            import exit
from bs4            import BeautifulSoup

import os
import json
import html


class Impex(object):
	def __init__(self):
		super(Impex, self).__init__()
		log.success('Iniciando gerador de impex: {proccess}'.format(proccess=os.getpid()))

		self.dumpFile    = 'data/notices/dump.json'
		self.impexHeader = '$contentCatalog=institutional{catalog}ContentCatalog\n$contentCV=catalogVersion(CatalogVersion.catalog(Catalog.id[default=$contentCatalog]),CatalogVersion.version[default=Staged])[default=$contentCatalog:Staged]\n$jarResourceCms=jar:net.weg.institucional.initialdata.setup.InitialDataSystemSetup&/weginstitucionalcore/import/cockpits/cmscockpit\n\n'
		self.notice      = "\n\nINSERT_UPDATE NewsPage;$contentCV[unique=true];uid[unique=true];masterTemplate(uid,$contentCV);title[lang='{language}'][default='{language}'];subtitle[lang='{language}'][default='{language}'];content[lang='{language}'][default='{language}'];category(code);tags(code);hiddentags(code);featured;publishdate[dateformat=dd/MM/yyyy];banner(code);defaultPage[default='true'];approvalStatus(code)[default='approved']\n;;{id};NewsPageTemplate;{title};{subtitle};'{content}';{category};;;{featured};{date};"

		if os.path.isfile(self.dumpFile):
			self.start()
		else:
			log.error('Dump de notícias não encontrado.')
			exit(0)


	def start(self):
		dump = open(self.dumpFile, 'r', encoding='utf-8').read()

		for notice in json.loads(dump):
			nid       = 'notice-{catalog}-'.format(catalog=notice['catalog'].upper()) + str(notice['id']).zfill(4)
			link      = notice['link']
			catalog   = 'data/notices/impex/'
			filename  = '{catalog}.impex'.format(catalog=notice['catalog'])
			impexFile = '{catalog}/{filename}'.format(catalog=catalog, filename=filename)

			impex = self.notice.format(
			 	id       = nid,
				title    = notice['title'],
				language = notice['language'],
				date     = notice['publishDate'],
				subtitle = notice['subtitle'],
				content  = self.parse(notice['content'], link),
				featured = str(notice['featured']).lower(),
				category = notice['category'],
			).strip()

			if os.path.isfile(impexFile):
				content = open(impexFile, encoding='utf-8').read()

				if nid in content:
					log.warning('Notícia já adicionada no impex [{nid}]'.format(nid=nid))
					return False
			try:
				with open(impexFile, mode='a+', encoding='utf-8') as file:
					if os.path.isfile(impexFile):
						file.write(self.impexHeader.format(catalog=notice['catalog'].capitalize()))
					file.write(impex)
				log.success('Notícia adicionada no impex [{id}]'.format(id=nid))
			except Exception as error:
				log.error(error)
				raise error


	def parse(self, content, link):
		document = BeautifulSoup(content.replace('\n', '').replace('\r', '').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"'), 'html.parser')
		toRemove = ['comparison', 'bgdark', 'bglight', 'default', 'clr', 'novaJanela']

		# tratamento posterior
		if document.select('.link-galeria'):
			print('*' * 200)
			print('trata galeria')
			print('*' * 200)

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
			tablefilename = helper.logs['tables']

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


if __name__ == '__main__':
	impex = Impex()
	log.success('Finalizando gerador de impex: {proccess}'.format(proccess=os.getpid()))