#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import __main__ as main
import time

class Logger(object):
	def __init__(self):
		super(Logger, self).__init__()


	@staticmethod
	def log(message, messageType='default', color='green'):
		if not message:
			return False

		now = time.strftime('%Y-%m-%d %H:%M:%S')

		colors = {
		    'red': '\033[0;31m',
		    'blue': '\033[0;34m',
		    'green': '\033[0;32m',
		    'white': '\033[1;37m',
		    'gray': '\033[0;37m',
		    'orange': '\033[0;33m',
		    'reset': '\033[0m'
		}

		if messageType == 'error':
			color = 'red'
		elif messageType == 'success':
			color = 'blue'
		elif messageType == 'warning':
			color = 'orange'

		message = '{color}[ {type} ]{reset} {gray}[{time}]{reset} {white}{message}{reset} [{file}]'.format(
			color = colors[color],
			type = ' ' + messageType.upper() + ' ' if messageType == 'error' else messageType.upper(),
			reset = colors['reset'],
			gray = colors['gray'],
			time = now, 
			white = colors['white'],
			message = message,
			file = main.__file__
		)

		print(message)

		return True


	@staticmethod
	def success(message):
		Logger.log(message, 'success')


	@staticmethod
	def error(message):
		Logger.log(message, 'error')


	@staticmethod
	def warning(message):
		Logger.log(message, 'warning')