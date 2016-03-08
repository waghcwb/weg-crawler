#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.generator import Generator as generator

import os


class Data(object):
	def __init__(self):
		super(Data, self).__init__()


	@staticmethod
	def get(item):
		data = Data
		if item == 'notices.list':
			data.getNotices()

	def getNotices():
		noticesFile = 'data/notices.json'

		if os.path.isfile(noticesFile):
			return open(noticesFile, 'r').read()
		else:
			generator.setNotices()