#!/usr/bin/env bash

set -e

files_to_remove=(
    'data/*.json'
    
    'data/news/images/notice-*'
    'data/news/impex/*.impex'
    
    'logs/20*.log'
    'logs/weg/*.list'

    'weg-*.zip'
)

make_reset () {
    x=0;

    while [ $x != ${#files_to_remove[@]} ]
    do
        _file=${files_to_remove[$x]}

        rm -rf ${_file}

        let "x = x +1"
    done

    echo 'Reset finalizado sem errors'
}

make_reset || echo 'Houve algum erro ao resetar os arquivos'