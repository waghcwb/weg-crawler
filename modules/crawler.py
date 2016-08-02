#!/usr/bin/env python3

from modules.logger import Logger as log
from modules.helper import Helper as helper
from bs4            import BeautifulSoup

import requests
import os
import modules.parser as parser

class Crawler( object ):
    def __init__( self ):
        super( Crawler, self ).__init__()

    def download_news( self, news ):
        init_crawling = '= Iniciando crawling, alvo: [ {nid} ] {link}'.format(nid=news['id'], link=os.path.basename( news['link'] ))

        print()

        log.success( '=' * len( init_crawling ) )
        log.success( init_crawling )
        log.success( '=' * len( init_crawling ) )

        print()

        request = requests.get( news['link'] )
        document = BeautifulSoup( request.text, 'html.parser' )

        if request.status_code == 200:
            return parser.parse_news( news, document )
        else:
            error_message = 'Erro ao acessar a página: Status {status_code}'.format(status_code=request.status_code)
            self.errors.append( error_message )
            log.error( error_message )