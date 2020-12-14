#!/bin/bash

cd /home/agurvets/alexgurvets.github.io/
python3 fetch_data.py
python3 frozen_flask.py
cp -R hackermd/src/build/* .
git add --all
git commit -m "automated update"
git push -u origin master