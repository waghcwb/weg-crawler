#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log

import sys
import os
import json
import shutil
import requests


class Helper(object):
	def __init__(self):
		super(Helper, self).__init__()


	@staticmethod
	def download(type, filename, nid, url):
		if type == 'image':
			try:
				response = requests.get(url, stream=True)

				with open(filename, 'wb') as image:
					shutil.copyfileobj(response.raw, image)
				log.success('Imagem baixada com sucesso [{url}]'.format(url=url))
			except Exception as error:
				log.error(error)
				pass


	@staticmethod
	def createFile(filename, content, mode='a+', format=None):
		os.chdir(sys.path[0])

		with open(filename, mode, encoding='utf-8') as file:
			if format == 'json':
				try:
					file.write(json.dumps(content, indent=4, sort_keys=True))
				except Exception as error:
					log.error(error.args[0])
					pass
			else:
				file.write(content)