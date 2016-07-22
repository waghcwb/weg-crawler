#!/usr/bin/env bash

folders_to_remove=(
	'data/images.json'
	'data/notices.json'
	'data/news/dump.json'
	'data/news/images/notice-*'
	'data/news/impex/*.impex'
	'logs/*.log'
	'logs/weg/notices.list'
	'logs/weg/tables.list'
	'weg-images.zip'
	'weg-impex.zip'
)

x=0;

while [ $x != ${#folders_to_remove[@]} ]
do
	folder=${folders_to_remove[$x]}

	echo "Pasta apagada: ${folder}"

	rm -rf ${folder}

	let "x = x +1"
done