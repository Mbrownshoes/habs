#!/bin/sh
set -x; exec 2>/tmp/mycommand.log

cd /projects/habs
python3 /projects/habs/load_data.py

git add .
git commit -am'updated yesterdays games'

git push origin gh-pages
