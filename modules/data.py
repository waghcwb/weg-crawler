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


	@staticmethod
	def getNotices():
		noticesFile = 'data/notices.json'

		if os.path.isfile(noticesFile):
			return json.loads( open(noticesFile, 'r').read() )
		else:
			return generator.setNotices()