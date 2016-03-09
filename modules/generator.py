#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log
from modules.helper import Helper as helper

import os
import sys
import re
import json


class Generator(object):
	def __init__(self):
		super(Generator, self).__init__()


	@staticmethod
	def setNotices():
		noticesListFile = 'data/notices.list'
		
		if os.path.isfile(noticesListFile):
			noticesList = open(noticesListFile, 'r') 
			catalog = None
			notices = []
			notice = 0

			for line in noticesList:
				if re.search('\[.*\]', line):
					catalog = line.replace('[', '').replace(']', '').replace('\n', '')
				else:
					line = line.replace('\n', '')
					if line:
						link = line.split(',')[0]
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

			return json.loads(notices)

		else:
			log.error('Lista de notícias para extrair não existe')
			sys.exit(0)