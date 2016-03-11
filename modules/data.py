#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.generator import Generator as generator

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


	@staticmethod
	def getImages():
		imagesFile = 'data/images.json'

		if os.path.isfile(imagesFile):
			return json.loads( open(imagesFile, 'r', encoding='utf-8').read() )
		else:
			return generator.setImagesList()


	@staticmethod
	def getNotices():
		noticesFile = 'data/notices.json'

		if os.path.isfile(noticesFile):
			return json.loads( open(noticesFile, 'r', encoding='utf-8').read() )
		else:
			return generator.setNotices()