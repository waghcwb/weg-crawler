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
		self.impexHeader = '$contentCatalog=institutional{catalog}ContentCatalog\n$contentCV=catalogVersion(CatalogVersion.catalog(Catalog.id[default=$contentCatalog]),CatalogVersion.version[default=Staged])[default=$contentCatalog:Staged]\n$jarResourceCms=jar:net.weg.institucional.initialdata.setup.InitialDataSystemSetup&/weginstitucionalcore/import/cockpits/cmscockpit\n'
		self.notice      = "\n\nINSERT_UPDATE NewsPage;$contentCV[unique=true];uid[unique=true];masterTemplate(uid,$contentCV);title[lang='{language}'][default='{language}'];subtitle[lang='{language}'][default='{language}'];content[lang='{language}'][default='{language}'];category(code);tags(code);hiddentags(code);featured;publishdate[dateformat=dd/MM/yyyy];banner(code);defaultPage[default='true'];approvalStatus(code)[default='approved']\n;;{id};NewsPageTemplate;{title};{subtitle};'{content}';{category};;;{featured};{date};"

		if os.path.isfile(self.dumpFile):
			self.start()
		else:
			log.error('Dump de notícias não encontrado.')
			exit(0)


	def start(self):
		dump = open(self.dumpFile, 'r', encoding='utf-8').read()

		for notice in json.loads(dump):
			try:
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
					content  = notice['content'],
					featured = notice['featured'],
					category = notice['category'],
				)

				if os.path.isfile(impexFile):
					content = open(impexFile, mode='r', encoding='utf-8').read()

					if nid in content:
						log.warning('Notícia já adicionada no impex [{nid}]'.format(nid=nid))
					else:
						with open(impexFile, mode='a+', encoding='utf-8') as file:
							file.write(impex)
						log.success('Notícia adicionada no impex [{id}]'.format(id=nid))
				else:
					with open(impexFile, mode='a+', encoding='utf-8') as file:
						file.write(self.impexHeader.format(catalog=notice['catalog'].capitalize()) + impex)
					log.success('Notícia adicionada no impex [{id}]'.format(id=nid))					

				

			except Exception as error:
				log.error(error.args[0])
				pass


if __name__ == '__main__':
	impex = Impex()
	log.success('Finalizando gerador de impex: {proccess}'.format(proccess=os.getpid()))