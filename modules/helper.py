#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os


class Helper(object):
	def __init__(self):
		super(Helper, self).__init__()


	@staticmethod
	def createFile(filename, content, mode='a+'):
		os.chdir(sys.path[0])

		with open(filename, mode, encoding='utf-8') as file:
		    file.write(content)