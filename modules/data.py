#!/usr/bin/env python3

from modules.logger  import Logger as log
from modules.helper  import Helper as helper
from modules.crawler import Crawler as crawler

import re
import os


class Data( crawler ):
    def __init__( self ):
        super( Data, self ).__init__()

        self.news_list_file = 'data/notices.list'
        self.news_json_file = 'data/notices.json'
        self.dump_file = 'data/dump.json'
        self.proccess = os.getpid()
        self.errors = []
        self.news_id_length = 4

        init_message = 'Iniciando processo: {proccess}'.format(proccess=self.proccess)
       
        log.success( '=' * len( init_message ) )
        log.success( init_message )
        log.success( '=' * len( init_message ) )
        print()

    def create_news_list( self ):
        news_list = helper.read_file(filename=self.news_list_file)
        news = []
        catalog = None
        nid = 0

        for line in news_list.split('\n'):
            if re.search('\[.*\]', line):
                catalog = line.replace('[', '').replace(']', '').replace('\n', '')
            else:
                if line:
                    notice   = 'notice-{catalog}-{id}'.format(catalog=catalog.upper(), id=str( nid ).zfill( self.news_id_length ))
                    link     = line.split(',')[0]
                    language = line.split(',')[1]
                    category = line.split(',')[2]

                    news.append({
                        'id': notice,
                        'link': link,
                        'language': language,
                        'category': category,
                        'errors': [],
                        'status': 'pending',
                        'catalog': catalog
                    })

                    nid += 1
        
        helper.create_file(filename='data/notices.json', content=news, format='json', mode='w')

        return news