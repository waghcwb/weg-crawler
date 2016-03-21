#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger    import Logger as log
from modules.generator import Generator as generator
from modules.helper    import Helper as helper
from modules.data      import Data as data
from sys               import exit

import os
import json
import requests
import shutil


class Images(object):
	def __init__(self):
		super(Images, self).__init__()

		self.imagesFile   = 'data/images.json'
		self.imagesFolder = 'data/notices/images/'
		self.dumpFile     = 'data/notices/dump.json'

		if os.path.isfile(self.imagesFile):
			self.start()
		else:
			log.error('Dump de imagens não existe.')

	def start(self):
		images = data.get('images')

		for index, image in enumerate(images, start=0):
			try:
				if not image['downloaded']:
					filename = os.path.basename(image['path'].replace('http://www.weg.net/', ''))
					folder   = self.imagesFolder + 'notice-{catalog}-'.format(catalog=image['catalog'].upper()) + str(image['id']).zfill(4)
					path     = '{folder}/{filename}'.format(folder=folder, filename=filename)

					if not os.path.isdir(folder):
						os.makedirs(folder, exist_ok=True)

					if helper.download(type='image', filename=path, nid=index, url=image['path']):
						images[index]['downloaded'] = True

				else:
					log.warning('Imagem já baixada [{url}]'.format(url=image['path']))
			except Exception as error:
				log.error(error)
				pass
			finally:
				helper.createFile(self.imagesFile, images, mode='w', format='json')


if __name__ == '__main__':
	images = Images()