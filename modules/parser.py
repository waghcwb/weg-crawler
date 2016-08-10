#!/usr/bin/env python3

from modules.logger import Logger as log
from modules.helper import Helper as helper
from datetime import datetime
from bs4 import BeautifulSoup

import os


def parse_news( news, document ):
    return {
        'id': news['id'],
        'title': get_title( document.select('.noticia-titulo h1') ),
        'subtitle': get_subtitle( document.select('.noticia-titulo h2') ),
        'content': get_content( news=news, content=document.select('.coluna5 .texto') ),
        'link': news['link'],
        'publishDate': get_timestamp( document.select('.noticia-detalhe .data') ),
        'banner': get_banner( document.select('.imagem-corpo-noticia img') ),
        'featured':    'false',
        'wegMagazine': '',
        'category': news['category'],
        'tags': get_tags( document.select('.tags a') ),
        'language': news['language'],
        'catalog': news['catalog']
    }

def get_title( title ):
    return str( title[0].string if title and title[0] else '' )

def get_subtitle( subtitle ):
    return str( subtitle[0].string if subtitle and subtitle[0] else '' )

def get_timestamp( publishDate ):
    timestamp = publishDate[0].attrs['date-timestamp'] if publishDate and publishDate[0] else 0
    return str( datetime.fromtimestamp(int( timestamp )).strftime('%d/%m/%Y') )

def get_banner( banner ):
    '''
        Banner está sendo tratado como imagem de layout, caso seja necessário adicionar no campo de banner será necessário criar um impex para adicionar a imagem no Hybris
        
        return str( banner[0].get('src') ) if banner and banner[0] else 'empty'
    '''
    return ''

def get_tags( tags ):
    return ', '.join(tag.string for tag in tags) if tags else ''

def get_content( news, content ):
    if not content[0]: return ''

    allowed_images_extension = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tif']
    document = BeautifulSoup( content[0].encode('utf-8'), 'html.parser' )
    to_remove = ['comparison', 'bgdark', 'bglight', 'default', 'clr', 'novaJanela']
    link = news['link']
    catalog = news['catalog']
    nid = news['id']

    for item in to_remove:
        if document.select('.{selector}'.format(selector=item)):
            for element in document.select('.{selector}'.format(selector=item)):
                index = element['class'].index( item )
                del element['class'][ index ]

    if document.select('.center'):
        for center in document.select('.center'):
            center['class'] = 'text-center'

    if document.select('p'):
        paragraphs = document.select('p')

        for paragraph in paragraphs:
            for content in paragraph.contents:
                if content == '\xa0' or not content:
                    paragraph.decompose()

    if document.select('table'):
            tables = document.select('table')
            tablefilename = 'logs/weg/tables.list'
            link = link if isinstance( link, str ) else link['href']

            for table in tables:
                to_remove = ['cellpadding', 'border', 'cellspacing', 'width', 'height']
                responsive = document.new_tag('div')
                responsive['class'] = 'table-responsive'
                table.wrap( responsive )

                table['class'].append('table table-bordered table-hover')

                for item in to_remove:
                    del table[ item ]

            if os.path.isfile( tablefilename ):
                content = helper.read_file( tablefilename )
                table_log = '[ {nid} ]: {link}\n'.format(link=link, nid=nid)

                if link not in content:
                    helper.create_file(tablefilename, table_log)
                else:
                    log.warning('Tabela já adicionada para a lista [ {url} ]'.format(url=link))
            else:
                helper.create_file(tablefilename, table_log)
                log.success('Log de tabelas criado.')

    if document.select('a'):
        for index, link in enumerate( document.select('a'), start=0 ):
            filename, file_extension = os.path.splitext( link.attrs['href'] )

            if link.attrs['href'] == 'javascript:void();':
                link.attrs['href'] = '#{nid}'.format(nid=news['id'])
                link.attrs['data-prevent-default'] = 'true'

            if file_extension in allowed_images_extension:
                set_image( news, index, link.attrs['href'] )
                link.attrs['href'] = set_image_link( news, index, link.attrs['href'] )

    if document.select('img'):
        for index, image in enumerate( document.select('img'), start=0 ):
            filename, file_extension = os.path.splitext( image.attrs['src'] )
            responsive = True

            if file_extension in allowed_images_extension:
                set_image( news, index, image.attrs['src'] )
                image.attrs['src'] = set_image_link( news, index, image.attrs['src'] )

            for parent in image.parents:
                if 'class' in parent.attrs:
                    if 'coluna6' in parent.attrs['class']:
                        responsive = False
            if responsive:
                if 'class' in image.attrs:
                    image.attrs['class'].append('img-responsive')
                else:
                    image.attrs['class'] = 'img-responsive'

    if document.select('.coluna6'):
        columns = document.select('.coluna6')

        for column in columns:
            column['class'] = 'xtt-gallery pull-right'

    if document.select('ul'):
        for ul in document.select('ul'):
            ul['class'] = 'xtt-list-style'

            for li in ul.select('> li'):
                span = document.new_tag('span')
                span.string = li.contents[0]
                li.string = ''
                li.append( span )

    return str( document ).strip()

def set_image( news, index, link ):
    images_file = 'data/images.json'
    images = helper.read_file( images_file, format='json' ) if os.path.isfile( images_file ) else []

    try:
        images.append({
            'catalog': news['catalog'],
            'notice': news['id'],
            'downloaded': False,
            'original_path': link,
            'new_path': set_image_link( news, index, link )
        })

        helper.create_file(images_file, images, mode='w', format='json')
        log.success('Imagem adicionada para a lista de downloads [ {image_link} ]'.format(image_link=set_image_link( news, index, link )))
    except Exception as error:
        log.error( error )


def set_image_link( news, index, link ):
    base_url  = 'https://static.weg.net'
    filename = os.path.basename( link )
    path = 'news/{nid}/{filename}'.format(nid=news['id'], filename=filename)
    parse_filename = path.split('.')
    parse_filename[0] = '{base_url}/{filename}_{suffix}'.format(base_url=base_url, filename=parse_filename[0][:255 - ( len( parse_filename[1] ) + len( base_url ) )], suffix=str( index ).zfill(4))
    filename = '.'.join( parse_filename )

    return filename