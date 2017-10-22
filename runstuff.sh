#!/bin/sh
cd /projects/habs


python load_data.py

git commit -am'updated yesterdays games'

git push orign gh-pages