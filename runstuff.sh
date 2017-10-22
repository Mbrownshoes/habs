#!/bin/sh
cd /projects/habs


"#python load_data.py"
touch readme.md

git commit -am'updated yesterdays games'

git push origin gh-pages
