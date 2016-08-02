#!/usr/bin/env bash

ROOT_FOLDER=$(pwd)

./reset.sh && ./scrapper.py && ./images.py && ./impex.py

cd $ROOT_FOLDER/data/news/images
zip -r $ROOT_FOLDER/weg-images.zip . -x *.git*

cd $ROOT_FOLDER/data/news/impex
zip -r $ROOT_FOLDER/weg-impex.zip . -x *.git*

cd $ROOT_FOLDER/logs

zip -r $ROOT_FOLDER/weg-logs.zip . -x *.git*