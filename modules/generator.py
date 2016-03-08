#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log

import os
import sys


class Generator(object):
	def __init__(self):
		super(Generator, self).__init__()


	@staticmethod
	def setNotices():
		noticesListFile = 'data/notices.list'
		
		if os.path.isfile(noticesListFile):
			noticesList = open(noticesListFile, 'r')

			for line in noticesList:
				print(line)
		else:
			log.error('Lista de notícias para extrair não existe')
			sys.exit(0)