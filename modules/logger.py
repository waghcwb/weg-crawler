#!/usr/bin/env python3

import __main__ as main
import time


class Logger( object ):
	def __init__( self ):
		super( Logger, self ).__init__()

	@staticmethod
	def log(message, messageType='default', color='green'):
		if not message:
			return False

		now = time.strftime('%Y-%m-%d %H:%M:%S')
		message = str( message ).encode('utf-8')

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

		log = '[ {type} ] [{time}] {message}\n'.format(
			type = ' ' + messageType.upper() + ' ' if messageType == 'error' else messageType.upper(),
			time = now,
			message = message.decode('utf-8')
		)

		message = '{color}[ {type} ]{reset} {gray}[{time}]{reset} {white}{message}{reset} [{file}]'.format(
			color = colors[ color ],
			type = ' ' + messageType.upper() + ' ' if messageType == 'error' else messageType.upper(),
			reset = colors['reset'],
			gray = colors['gray'],
			time = now, 
			white = colors['white'],
			message = message.decode('utf-8'),
			file = main.__file__
		)

		print( message )

		with open('logs/{time}.log'.format(time=time.strftime('%Y-%m-%d')), 'a+', encoding='utf-8') as file:
			file.write(log)

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