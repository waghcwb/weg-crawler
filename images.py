#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger    import Logger as log
from modules.generator import Generator as generator
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
		self.imagesFolder = 'data/notices/images'
		self.dumpFile     = 'data/notices/dump.json'

		images = data.getImages()

		for image in images:
			filename = '{folder}/{notice}/{image}'.format(folder=self.imagesFolder, notice=image['notice'], image=image['path'].split('/')[-1])
			self.download(image['path'], filename)

	def download(self, link, filename):
		try:
			response = requests.get(link, stream=True)
			folder = os.path.dirname(filename)
			
			if not os.path.isdir(folder):
				os.makedirs(folder)

			with open(filename, 'wb') as image:
				shutil.copyfileobj(response.raw, image)
				log.success('Imagem baixada com sucesso [{image}]'.format(image=filename))
		except Exception as error:
			log.error(error)
			raise error


if __name__ == '__main__':
	images = Images()