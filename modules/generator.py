#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log
from modules.helper import Helper as helper
from sys            import exit
from bs4            import BeautifulSoup

import os
import re
import json


class Generator(object):
	def __init__(self):
		super(Generator, self).__init__()


	@staticmethod
	def setImagesList():
		dumpFile   = 'data/notices/dump.json'
		imagesFile = 'data/images.json'
		images = []
		dump = json.loads( open(dumpFile, 'r', encoding='utf-8').read() )

		if os.path.isfile(imagesFile):
			images = json.loads( open(imagesFile, 'r', encoding='utf-8').read() )

		for notice in dump:
			document = BeautifulSoup(notice['content'], 'html.parser')

			if notice['banner'] != 'empty':
				images.append({
					'catalog': notice['catalog'],
					'downloaded': False,
					'notice': 'notice-{catalog}-'.format(catalog=notice['catalog'].upper()) + str(notice['id']).zfill(4),
					'path': notice['banner'] if notice['banner'].startswith('http') else 'http://www.weg.net{path}'.format(path=notice['banner']),
					'type': 'banner'
				})

			if document.select('img'):
				for image in document.select('img'):
					try:
						if image.get('src') in str(images):
							log.warning('Imagem já adicionada para a lista [{link}]'.format(link=image.get('src')))
						else:
							images.append({
								'catalog': notice['catalog'],
								'downloaded': False,
								'notice': 'notice-{catalog}-'.format(catalog=notice['catalog'].upper()) + str(notice['id']).zfill(4),
								'path': image.get('src') if image.get('src').startswith('http') else 'http://www.weg.net{path}'.format(path=image.get('src')),
								'type': 'image'
							})
					except Exception as error:
						raise error
					finally:
						with open(imagesFile, 'w+', encoding='utf-8') as file:
							file.write(json.dumps(images, indent=4, sort_keys=True))
						log.success('Imagem adicionada para a lista [{link}]'.format(link=image.get('src')))
			return images


	@staticmethod
	def setNotices():
		noticesListFile = 'data/notices.list'

		if os.path.isfile(noticesListFile):
			noticesList = open(noticesListFile, 'r', encoding='utf-8') 
			catalog     = None
			notices     = []
			notice      = 0

			for line in noticesList:
				if re.search('\[.*\]', line):
					catalog = line.replace('[', '').replace(']', '').replace('\n', '')
				else:
					line = line.replace('\n', '')
					if line:
						link     = line.split(',')[0]
						language = line.split(',')[1]
						category = line.split(',')[2]

						notices.append({
							'id': notice,
							'link': link,
							'language': language,
							'category': category,
							'errors': [],
							'status': 'pending',
							'catalog': catalog
						})

						notice += 1
			helper.createFile('data/notices.json', json.dumps(notices, indent=4, sort_keys=True), mode='w')

			return notices

		else:
			log.error('Lista de notícias para extrair não existe')
			exit(0)