#!/bin/bash
date
set -e
set -x
cd /Users/alexgurvets/projects/hackermd-github-pages/agurvets.github.io
whoami
git pull
# Requires ANTHROPIC_API_KEY to be set in the environment
pip3 install requests Frozen-Flask humanize anthropic
python3 fetch_data.py
python3 frozen_flask.py
cp -R hackermd/src/build/* .
git add --all
git commit -m "automated update"
git push -u origin master