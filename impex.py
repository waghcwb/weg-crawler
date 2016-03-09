#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Impex(object):
	def __init__(self):
		super(Impex, self).__init__()
		log.success('Iniciando gerador de impex: {proccess}'.format(proccess=os.getpid()))


	def create(self):
		pass


if __name__ == '__main__':
	impex = Impex()
	impex.start()
	log.success('Finalizando gerador de impex: {proccess}'.format(proccess=os.getpid()))