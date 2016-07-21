#!/usr/bin/env python3

from modules.helper import Helper as helper
from modules.logger import Logger as log
from sys            import exit
from bs4            import BeautifulSoup

import os
import json


class Impex(object):
    def __init__(self):
        super(Impex, self).__init__()
        log.success('Iniciando gerador de impex: {proccess}'.format(proccess=os.getpid()))

        self.dumpFile    = 'data/news/dump.json'
        self.impexHeader = '$contentCatalog=institutional{catalog}ContentCatalog\n$contentCV=catalogVersion(CatalogVersion.catalog(Catalog.id[default=$contentCatalog]),CatalogVersion.version[default=Staged])[default=$contentCatalog:Staged]\n$jarResourceCms=jar:net.weg.institucional.initialdata.setup.InitialDataSystemSetup&/weginstitucionalcore/import/cockpits/cmscockpit\n'
        self.notice      = "\n\nINSERT_UPDATE NewsPage;$contentCV[unique=true];uid[unique=true];masterTemplate(uid,$contentCV);name;title[lang={language}][allownull=true];subtitle[lang={language}][allownull=true];content[lang={language}][allownull=true];category(code);tags(code);hiddentags(code);featured;publishdate[dateformat=dd/MM/yyyy];banner(code);defaultPage[default='true'];approvalStatus(code)[default='approved']\n;;{id};NewsPageTemplate;{name};{title};{subtitle};\"{content}\";{category};;;{featured};{date}"

        if os.path.isfile(self.dumpFile):
            self.start()
        else:
            log.error('Dump de notícias não encontrado.')
            exit(0)


    def start(self):
        content = helper.readFile(self.dumpFile, format='json')

        for notice in content:
            try:
                nid          = 'notice-{catalog}-'.format(catalog=notice['catalog'].upper()) + str(notice['id']).zfill(4)
                link         = notice['link']
                catalog      = 'data/news/impex/'
                filename     = '{catalog}-{language}.impex'.format(catalog=notice['catalog'], language=notice['language'])
                impexFile    = '{catalog}/{filename}'.format(catalog=catalog, filename=filename)
                ellipses     = '...'
                maxTitleSize = 140 - len( ellipses )
                maxNameSize  = 255 - len( ellipses )

                impex = self.notice.format(
                    id       = nid,
                    title    = notice['title'] if len( notice['title'] ) < maxTitleSize else notice['title'][:maxTitleSize] + ellipses,
                    name     = notice['title'] if len( notice['title'] ) < maxNameSize else notice['title'][:maxNameSize] + ellipses,
                    language = notice['language'],
                    date     = notice['publishDate'],
                    subtitle = notice['subtitle'] if len( notice['subtitle'] ) < maxTitleSize else notice['subtitle'][:maxTitleSize] + ellipses,
                    content  = notice['content'],
                    featured = notice['featured'],
                    category = notice['category']
                )

                if os.path.isfile(impexFile):
                    content = helper.readFile(impexFile)

                    if nid in content:
                        log.warning('Notícia já adicionada no impex [{nid}]'.format(nid=nid))
                    else:
                        helper.createFile(impexFile, impex)
                        log.success('Notícia adicionada no impex [{id}]'.format(id=nid))
                else:
                    helper.createFile(impexFile, self.impexHeader.format(catalog=notice['catalog'].capitalize()) + impex)
                    log.success('Notícia adicionada no impex [{id}]'.format(id=nid))                    
            except Exception as error:
                log.error(error)
                pass


if __name__ == '__main__':
    impex = Impex()
    log.success('Finalizando gerador de impex: {proccess}'.format(proccess=os.getpid()))