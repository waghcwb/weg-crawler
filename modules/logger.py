#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Logger(object):
	def __init__(self):
		super(Logger, self).__init__()


	@staticmethod
	def log(message, messageType='default'):
		print(message)


	@staticmethod
	def warning(message):
		Logger.log(message, 'warning')