#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log
from sys import exit

import os
import json


class Impex(object):
	def __init__(self):
		super(Impex, self).__init__()
		log.success('Iniciando gerador de impex: {proccess}'.format(proccess=os.getpid()))

		self.dumpFile    = 'data/notices/dump.json'
		self.impexHeader = '$contentCatalog=institutional{catalog}ContentCatalog\n$contentCV=catalogVersion(CatalogVersion.catalog(Catalog.id[default=$contentCatalog]),CatalogVersion.version[default=Staged])[default=$contentCatalog:Staged]\n$jarResourceCms=jar:net.weg.institucional.initialdata.setup.InitialDataSystemSetup&/weginstitucionalcore/import/cockpits/cmscockpit\n\n'
		self.notice      = "\n\nINSERT_UPDATE NewsPage;$contentCV[unique=true];uid[unique=true];masterTemplate(uid,$contentCV);title[lang={language}];subtitle[lang={language}];content[lang={language}];category(code);tags(code);hiddentags(code);featured;publishdate[dateformat=dd/MM/yyyy];banner(code);defaultPage[default='true'];approvalStatus(code)[default='approved']\n;;{id};NewsPageTemplate;{title};{subtitle};'{content}';{category};;;{featured};{date};"

		if os.path.isfile(self.dumpFile):
			self.start()
		else:
			log.error('Dump de notícias não encontrado.')
			exit(0)


	def start(self):
		dump = open(self.dumpFile, 'r').read()

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
				content = open(impexFile).read()

				if nid in content:
					log.warning('Notícia já adicionada no impex [{nid}]'.format(nid=nid))
					return False
			try:
				with open(impexFile, mode='a+') as file:
					if os.path.isfile(impexFile):
						file.write(self.impexHeader.format(catalog=catalog.capitalize()))
					file.write(impex)
				log.success('Notícia adicionada no impex [{id}]'.format(id=nid))
			except Exception as error:
				log.error(error)
				raise error

	def parse(self, impex, link):
		pass


if __name__ == '__main__':
	impex = Impex()
	log.success('Finalizando gerador de impex: {proccess}'.format(proccess=os.getpid()))