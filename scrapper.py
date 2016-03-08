#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.logger import Logger as log
from modules.data import Data as data

import os


class Scrapper(object):
	def __init__(self):
		super(Scrapper, self).__init__()

		log.success('Iniciando processo: {proccess}'.format(proccess=os.getpid()))


	def start(self):
		noticesList = data.get('notices.list')


if __name__ == '__main__':
	scrapper = Scrapper()
	scrapper.start()
	log.success('Finalizando processo: {proccess}'.format(proccess=os.getpid()))