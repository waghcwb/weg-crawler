#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.generator import Generator as generator
from modules.data import Data as data
from sys import exit

import os
import json


class Images(object):
	def __init__(self):
		super(Images, self).__init__()

		self.imagesFile = 'data/images.json'
		self.dumpFile   = 'data/notices/dump.json'

		if os.path.isfile(self.imagesFile):
			json.loads( open(self.imagesFile, 'r').read() )
		elif os.path.isfile(self.dumpFile):
			images = data.getImages()

			print(images)
		else:
			log.error('Arquivo de dump não encontrado.')
			exit(0)


if __name__ == '__main__':
	images = Images()