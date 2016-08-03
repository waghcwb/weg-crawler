#!/usr/bin/env bash

files_to_remove=(
    'data/*.json'
    
    'data/news/images/notice-*'
    'data/news/impex/*.impex'
    
    'logs/*.log'
    'logs/weg/*.list'

    'weg-images.zip'
    'weg-impex.zip'
    'weg-logs.zip'
)

x=0;

while [ $x != ${#files_to_remove[@]} ]
do
    _file=${files_to_remove[$x]}

    if [ ! -s ${_file} ]; then
        echo "[ ! ] Arquivo inexistente - ${_file}"
    elif [ -d ${_file} ]; then
        echo "[ ✔ ] Diretório apagado - ${_file}"
        rm -rf ${_file}
    else
        echo "[ ✔ ] Arquivo apagado - ${_file}"
        rm ${_file}
    fi

    let "x = x +1"
done