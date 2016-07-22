#!/usr/bin/env python3

# when things starting to going bad ..

import html
import os

from modules.helper    import Helper    as helper
from modules.logger    import Logger    as log
from modules.generator import Generator as generator
from modules.data      import Data      as data
from bs4               import BeautifulSoup


class Fixer( object ):
	def __init__( self ):
		super( Fixer, self ).__init__()

		self.dumpFile    = 'data/news/dump.json'

		if os.path.isfile(self.dumpFile):
			self.gallery_links()
			self.responsive_images()
		else:
			log.error('Arquivo de dump não existe.')


	def responsive_images( self ):
		dump = data.get('dump')

		for index, item in enumerate(dump, start=0):
			document = BeautifulSoup(item['content'].replace('""', '"'), 'html.parser')

			if document.find('img'):
				images = document.select('img')

				for image in images:
					image['class'] = 'img-responsive'
					dump[ index ]['content'] = str( document )

					helper.createFile('data/news/dump.json', dump, mode='w', format='json')


	def gallery_links( self ):
		dump = data.get('dump')

		for index, item in enumerate(dump, start=0):
			document = BeautifulSoup(item['content'].replace('""', '"'), 'html.parser')
			baseURL  = 'http://static.weg.net'
			imageBaseURL = 'news/'

			if document.select('a[rel="image-zoom"]'):
				links = document.select('a[rel="image-zoom"]')

				for link in links:
					filename = os.path.basename(link['href'].replace('http://www.weg.net/', ''))
					folder   = imageBaseURL + 'notice-{catalog}-'.format(catalog=item['catalog'].upper()) + str(item['id']).zfill(4)
					path     = '{folder}/{filename}'.format(folder=folder, filename=filename)

					link.attrs['href'] = '{base}/{filename}'.format(base=baseURL, filename=path)

					generator.setImage(link, item['id'], item['catalog'])
					dump[ index ]['content'] = str( document )
					helper.createFile('data/news/dump.json', dump, mode='w', format='json')


if __name__ == '__main__':
	Fixer()