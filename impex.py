#!/usr/bin/env python3

from modules.logger    import Logger as log
from modules.helper    import Helper as helper

import os


class Impex( object ):
    def __init__( self ):
        super( Impex, self ).__init__()

        self.dump_file = 'data/dump.json'
        self.impex_folder = 'data/news/impex'
        self.impex_header = '$contentCatalog=institutional{catalog}ContentCatalog\n$contentCV=catalogVersion(CatalogVersion.catalog(Catalog.id[default=$contentCatalog]),CatalogVersion.version[default=Staged])[default=$contentCatalog:Staged]\n$jarResourceCms=jar:net.weg.institucional.initialdata.setup.InitialDataSystemSetup&/weginstitucionalcore/import/cockpits/cmscockpit\n'
        self.impex_content = "\n\nINSERT_UPDATE NewsPage;$contentCV[unique=true];uid[unique=true];masterTemplate(uid,$contentCV);name;title[lang={language}][allownull=true];subtitle[lang={language}][allownull=true];content[lang={language}][allownull=true];category(code);tags(code);hiddentags(code);featured;publishdate[dateformat=dd/MM/yyyy];banner(code);defaultPage[default='true'];approvalStatus(code)[default='approved']\n;;{id};NewsPageTemplate;{name};{title};{subtitle};\"{content}\";{category};;;{featured};{date}"

        if os.path.isfile( self.dump_file ):
            notices = helper.read_file( self.dump_file, format='json' )

            for news in notices:
                try:
                    nid = news['id']
                    ellipses     = '...'
                    max_title_size = 140 - len( ellipses )
                    max_name_size  = 255 - len( ellipses )
                    filename     = '{catalog}-{language}.impex'.format(catalog=news['catalog'], language=news['language'])
                    folder = '{folder}/{catalog}/'.format(folder=self.impex_folder, catalog=news['catalog'])
                    impex_file = '{folder}/{catalog}/{filename}'.format(folder=self.impex_folder, catalog=news['catalog'], filename=filename)
                     

                    impex = self.impex_content.format(
                        id       = nid,
                        title    = news['title'] if len( news['title'] ) < max_title_size else news['title'][:max_title_size] + ellipses,
                        name     = news['title'] if len( news['title'] ) < max_name_size else news['title'][:max_name_size] + ellipses,
                        language = news['language'],
                        date     = news['publishDate'],
                        subtitle = news['subtitle'] if len( news['subtitle'] ) < max_title_size else news['subtitle'][:max_title_size] + ellipses,
                        content  = news['content'].replace('"', '""'),
                        featured = news['featured'],
                        category = news['category']
                    )

                    if not os.path.isdir(folder):
                        os.makedirs(folder, exist_ok=True)

                    if os.path.isfile( impex_file ):
                        content = helper.read_file( impex_file )

                        if nid in content:
                            log.warning('Notícia já adicionada no impex [{nid}]'.format(nid=nid))
                        else:
                            helper.create_file(impex_file, impex)
                            log.success('Notícia adicionada no impex [{id}]'.format(id=nid))
                    else:
                        helper.create_file(impex_file, self.impex_header.format(catalog=news['catalog'].capitalize()) + impex)
                        log.success('Notícia adicionada no impex [{id}]'.format(id=nid))
                except Exception as error:
                    log.error( error )
        else:
            log.error('[!] Dump de notícias não existe')


if __name__ == '__main__': Impex()      