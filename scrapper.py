#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log

class Scrapper(object):
	def __init__(self):
		super(Scrapper, self).__init__()

	def start(self):
		log.warning('ok')
		
if __name__ == '__main__':
	scrapper = Scrapper()
	scrapper.start()