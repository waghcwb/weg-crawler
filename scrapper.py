#!/usr/bin/env python3

from modules.logger  import Logger as log
from modules.data    import Data as data
from modules.crawler import Crawler as crawler
from modules.helper  import Helper as helper

import os
import time


class Scrapper( object ):
    def __init__( self ):
        super( Scrapper, self ).__init__()

        log.success('Iniciando processo: {proccess}'.format(proccess=os.getpid()))


    def start( self ):
        notices_list = data.get('notices.list')
        notices = []

        for index, notice in enumerate( notices_list, start=0 ):
            nid          = notice['id']
            link         = notice['link']
            category     = notice['category']
            errors       = notice['errors']
            status       = notice['status']
            language     = notice['language']
            catalog      = notice['catalog']
            init_message = 'Iniciando crawling, alvo: {url}'.format(url=os.path.basename(link))

            if status == 'pending':
                if errors:
                    log.error('[{nid}] Tratar erros: {errors}'.format(nid=nid, errors=errors))
                else:
                    try:
                        print()
                        log.success( init_message )
                        log.success( '*' * len( init_message ) )

                        content = crawler.getData(nid, category, language, catalog, link)

                        if not content:
                            raise ValueError('Título, subtítulo ou conteúdo não encontrados no documento: {url}'.format(url=link))
                        elif content == 404:
                            raise ValueError('Página não encontrada')
                        else:
                            notices_list[ index ]['status'] = 'completed'
                            notices.append( content )

                            helper.createFile('data/news/dump.json', notices, mode='w', format='json')
                            helper.createFile('logs/weg/notices.list', '[notice-{uid}] {notice}\n'.format(uid=catalog.upper() + str(nid).zfill(4), notice=link))

                            log.success('[{nid}] Dados salvos com sucesso'.format(nid=nid))
                    except Exception as error:
                        log.error( error )
                        notices_list[index]['errors'].append( error )
                        pass
                    finally:
                        helper.createFile('data/notices.json', notices_list, mode='w', format='json')
                        log.success( '*' * len( init_message ) )
                        print()
                        # time.sleep(3)
            else:
                log.warning('Dados dessa notícia já foram adquiridos [{nid}]'.format(nid=nid))

            # Pegar só 1 notícia por enquanto.
            # if index == 1:
            #   exit(0)


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.start()
    log.success('Finalizando processo: {proccess}'.format(proccess=os.getpid()))