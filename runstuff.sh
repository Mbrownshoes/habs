#!/bin/sh
set -x; exec 2>/tmp/mycommand.log
keychain id_rsa id_dsa
. ~/.keychain/`uname -n`-sh
 
cd /projects/habs
python3 /projects/habs/load_data.py

git add .
git commit -am'updated yesterdays games'

git push origin gh-pages
