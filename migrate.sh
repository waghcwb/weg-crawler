#!/usr/bin/env bash

./reset.sh && ./scrapper.py && ./images.py && ./impex.py

cd data/news/images

zip -r ../../../weg-images.zip . -x *.git*

cd ../impex

zip -r ../../../weg-impex.zip . -x *.git*