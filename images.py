#!/usr/bin/env python3

from modules.logger    import Logger as log
from modules.helper    import Helper as helper
from sys               import exit

import os


class Images( object ):
    def __init__( self ):
        super( Images, self ).__init__()

        self.images_file = 'data/images.json'
        self.images_folder = 'data/news/images/'
        self.dump_file     = 'data/news/dump.json'

        if os.path.isfile( self.images_file ):
            images = helper.read_file( self.images_file, format='json' )

            for index, image in enumerate(images, start=0):
                try:
                    if not image['downloaded']:
                        path = 'data/{image_path}'.format(image_path=image['new_path'].replace('http://static.weg.net/', ''))
                        filename = os.path.basename( path )
                        folder = path.split('/')
                        folder.pop()
                        folder = '/'.join( folder )
                        base_url = 'http://www.weg.net'
                        download_url = image['original_path']

                        if not os.path.isdir( folder ):
                            os.makedirs(folder, exist_ok=True)

                        if not download_url.startswith('http'):
                            download_url = '{base_url}/{path}'.format(base_url=base_url, path=download_url)

                        if helper.download(type='image', filename=path, nid=index, url=download_url):
                            images[ index ]['downloaded'] = True
                            log.success('Imagem baixada com sucesso [ {path} ]'.format(path=path))
                    else:
                        log.warning('Imagem já baixada [ {url} ]'.format(url=image['new_path']))
                except Exception as error:
                    log.error( error )
                finally:
                    helper.create_file(self.images_file, images, mode='w', format='json')
        else:
            log.error('[!] Dump de imagens não existe')


if __name__ == '__main__': Images()        