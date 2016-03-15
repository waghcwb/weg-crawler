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
	def createFile(filename, content, mode='a+', encoding='utf-8', format=None):
		os.chdir(sys.path[0])

		try:
			if format == 'json':
				content = json.dumps(content, indent=4, sort_keys=True)

			_file = open(filename, mode=mode, encoding=encoding)
			_file.write(content)
			_file.close()
		except Exception as error:
			log.error(error.args[0])
			pass


	@staticmethod
	def readFile(filename, format=None, mode='r', encoding='utf-8'):
		os.chdir(sys.path[0])

		if not os.path.isfile(filename):
			log.error('O arquivo não existe [{file}]'.format(file=filename))
			return None
		else:
			try:
				_file = open(filename, mode=mode, encoding=encoding)
				_content = _file.read()
				_file.close()

				if format == 'json':
					return json.loads(_content)
				else:
					return _content
			except Exception as error:
				log.error(error.args[0])
				pass