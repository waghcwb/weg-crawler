#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.generator import Generator as generator
from modules.helper    import Helper as helper

import os
import json


class Data(object):
	def __init__(self):
		super(Data, self).__init__()

	@staticmethod
	def get(item):
		if item == 'notices.list':
			return Data.getNotices()

		if item == 'images':
			return Data.getImages()

		if item == 'dump':
			return Data.getDump()


	@staticmethod
	def getImages():
		imagesFile = 'data/images.json'

		if os.path.isfile(imagesFile):
			return helper.readFile(imagesFile, format='json')
		else:
			return generator.setImagesList()


	@staticmethod
	def getNotices():
		noticesFile = 'data/notices.json'

		if os.path.isfile(noticesFile):
			return helper.readFile(noticesFile, format='json')
		else:
			return generator.setNotices()


	@staticmethod
	def getDump():
		dumpFile = 'data/news/dump.json'

		if os.path.isfile('data/news/dump.json'):
			return helper.readFile(dumpFile, format='json')
		else:
			return False
		