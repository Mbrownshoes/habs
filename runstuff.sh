#!/bin/sh
cd /projects/habs


python projects/habs/load_data.py

git add .
git commit -am'updated yesterdays games'

git push origin gh-pages
