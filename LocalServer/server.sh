#!/bin/sh
cd /usr/local/etc/pkg/repos/
python3.7 /root/installCIF/LocalServer/editConf.py
pkg update
yes | pkg install py38-pip
cd
cd /root/installCIF/LocalServer/
python3.7 -m venv venv
#sudo ./venv/bin/activate
yes | pip-3.8 install Flask
yes | pip-3.8 install plotly
pip-3.8 install wheel
pip-3.8 install gunicorn
yes | pkg install databases/py-sqlite3
set path= /usr/local/lib/python3.8/site-packages $path
gunicorn --bind 0.0.0.0:5000 wsgi:app &
