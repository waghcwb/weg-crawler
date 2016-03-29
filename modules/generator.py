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
	def setImage(image, nid, catalog):
		imagesFile = 'data/images.json'
		images = helper.readFile(imagesFile, format='json') if os.path.isfile(imagesFile) else []
		imagename = image.get('src') if image.name == 'img' else image.get('href')
		baseurl = 'http://www.weg.net'

		if not imagename.startswith('http'):
			imagename = baseurl + imagename

		try:
			if not imagename in json.dumps(images):
				images.append({
					'id': nid,
					'catalog': catalog,
					'downloaded': False,
					'notice': 'notice-{catalog}-'.format(catalog=catalog.upper()) + str(nid).zfill(4),
					'path': imagename,
					'type': 'image'
				})

				log.success('Imagem setada [{url}]'.format(url=imagename))
			else:
				log.warning('Imagem já adicionada para fazer download [{url}]'.format(url=imagename))
		except Exception as error:
			log.error('Erro ao adicionar a imagem para a lista [{url}]'.format(url=imagename))
			log.error(error.args[0])
			pass
		finally:
			helper.createFile(imagesFile, images, mode='w', format='json')
			pass


	@staticmethod
	def setImagesList():
		dumpFile   = 'data/news/dump.json'
		imagesFile = 'data/images.json'
		images     = helper.readFile(imagesFile, format='json') if os.path.isfile(imagesFile) else []
		dump       = helper.readFile(dumpFile, format='json')

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
						helper.createFile(imagesFile, images, mode='w+', format='json')
						log.success('Imagem adicionada para a lista [{link}]'.format(link=image.get('src')))
			else:
				log.warning('Notícia sem imagens')

			return images


	@staticmethod
	def setNotices():
		noticesListFile = 'data/notices.list'

		if os.path.isfile(noticesListFile):
			noticesList = helper.readFile(noticesListFile)
			catalog     = None
			notices     = []
			notice      = 0

			for line in noticesList.split('\n'):
				if re.search('\[.*\]', line):
					catalog = line.replace('[', '').replace(']', '').replace('\n', '')
				else:
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
			
			helper.createFile('data/notices.json', notices, mode='w', format='json')

			return notices

		else:
			log.error('Lista de notícias para extrair não existe')
			exit(0)