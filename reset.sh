#!/usr/bin/env bash

folders_to_remove=(
	'data/news/images/*'
	'data/images.json'
	'data/news/impex/*'
	'data/news/dump.json'
	'data/notices.json'
	'logs/tables/*'
	'logs/tags/*'
)

x=0;

while [ $x != ${#folders_to_remove[@]} ]
do
	folder=${folders_to_remove[$x]}

	echo "Pasta apagada: ${folder}"

	rm -rf ${folder}

	let "x = x +1"
done