#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log
from modules.data   import Data as data
from modules.crawler import Crawler as crawler
from modules.helper import Helper as helper

import os
import json


class Scrapper(object):
	def __init__(self):
		super(Scrapper, self).__init__()

		log.success('Iniciando processo: {proccess}'.format(proccess=os.getpid()))


	def start(self):
		noticesList = data.get('notices.list')
		notices = []

		for index, notice in enumerate(noticesList, start=0):
			nid      = notice['id']
			link     = notice['link']
			category = notice['category']
			errors   = notice['errors']
			status   = notice['status']
			language = notice['language']
			catalog  = notice['catalog']

			if status == 'pending':
				if errors:
					log.error('[{nid}] Tratar erros: {errors}'.format(nid=nid, errors=errors))
				else:
					try:
						log('Iniciando crawling, alvo: {link}'.format(link=link))

						html = crawler.request(link)

						print(html)

					except Exception as error:
						log.error(error)
						data[index]['errors'].append(error)
						pass
					finally:
						print('*' * 100)
						print(notices)
						print( type(notices) )
						print('*' * 100)
						helper.createFile('data/notices.json', json.dumps(notices, indent=4, sort_keys=True))
			else:
				log.warning('Dados dessa notícia já foram adquiridos [{nid}]'.format(nid=nid))

			# Pegar só 1 notícia por enquanto.
			return

if __name__ == '__main__':
	scrapper = Scrapper()
	scrapper.start()
	log.success('Finalizando processo: {proccess}'.format(proccess=os.getpid()))