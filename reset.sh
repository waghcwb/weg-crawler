#!/usr/bin/env bash

folders_to_remove=(
	'data/*.json'
	'data/news/impex/*'
	'data/news/images/notice-*'
	'logs/weg/*'
	'logs/tags/*.json'
	'logs/201*.log'
	'weg-images.zip'
	'weg-impex.zip'
	'weg-logs.zip'
)



x=0;

while [ $x != ${#folders_to_remove[@]} ]
do
	folder=${folders_to_remove[$x]}

	echo "Pasta apagada: ${folder}"

	rm -rf ${folder}

	let "x = x +1"
done