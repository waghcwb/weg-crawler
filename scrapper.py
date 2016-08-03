#!/usr/bin/env python3

__brand__ = 'WEG Crawler'
__author__ = 'Wagner Souza'
__description__ = 'Data scraper for WEG Site'
__version__ = '1.0.0'

from modules.data    import Data   as data
from modules.logger  import Logger as log
from modules.helper  import Helper as helper

import os


class Scrapper( data ):
    def __init__( self ):
        super( Scrapper, self ).__init__()

        if not os.path.isfile( self.news_list_file ):
            return exit('Lista para extração de dados não encontrada.')

        self.news_list = helper.read_file( filename=self.news_json_file, format='json' ) or self.create_news_list()
        self.news = helper.read_file( filename=self.dump_file, format='json' ) or []

    def start( self ):
        for index, news in enumerate( self.news_list, start=0 ):
            try:
                if news['status'] == 'pending':
                    news_content = self.download_news( news )

                    if news_content:
                        self.news_list[ index ]['status'] = 'completed'
                        self.news.append( news_content )

                        log.success('[ {nid} ] Dados salvos com sucesso!'.format(nid=news['id']))

                        print()
                        print()
                    else:
                        error_message = 'Não foi possível fazer o parse dos dados.'
                        log.error( error_message )
                        self.errors.append( error_message )
                        self.news_list[ index ]['errors'].append( error_message )
                else:
                    log.warning('Dados já adquiridos [ {nid} ]'.format(nid=news['id']))
            except Exception as error:
                log.error('Erro ao baixar a notícia [ {nid} ]'.format(nid=news['id']))
                log.error(error)
                pass
            finally:
                helper.create_file( filename=self.dump_file, content=self.news, format='json', mode='w')
                helper.create_file( filename=self.news_json_file, content=self.news_list, format='json', mode='w')


if __name__ == '__main__':
    scrapper = Scrapper()

    try:
        scrapper.start()
    except Exception as error:
        print()
        error_message = 'Erro ao iniciar processo: {proccess}'.format(proccess=scrapper.proccess)
        log.error('=' * len( error_message ))
        log.error( error_message )
        log.error(error)
        log.error('=' * len( error_message ))
        print()
    finally:
        finished_with_errors = 'Finalizado com {errors} erro{suffix}'.format(errors=len( scrapper.errors ), suffix='s' if len( scrapper.errors ) > 1 else '')
        finished_without_errors = 'Finalizado sem erros'

        if scrapper.errors:
            print()
            log.warning( '=' * len( finished_with_errors ) )
            log.warning( finished_with_errors )
        else:
            print()
            log.success( '=' * len( finished_without_errors ) )
            log.success( finished_without_errors )