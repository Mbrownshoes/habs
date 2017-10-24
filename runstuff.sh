#!/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

touch xxx.txt

python projects/habs/load_data.py

git add .
git commit -am'updated yesterdays games'

git push origin gh-pages
