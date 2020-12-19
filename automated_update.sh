#!/bin/bash
date
set -e
set -x
cd /Users/alexgurvets/projects/hackermd-github-pages/agurvets.github.io
git pull
pip3 install requests Frozen-Flask humanize
/usr/bin/python3 fetch_data.py
/usr/bin/python3 frozen_flask.py
cp -R hackermd/src/build/* .
git add --all
git commit -m "automated update"
git push -u origin master