#!/bin/bash -i
chmod +x install.sh makeConfigFile.py path.py
yes | sudo apt update
yes | sudo apt install python3-pip
python3 -m pip install 'cifsdk>=3.0.0,<4.0'
python3 makeConfigFile.py
mv .cif.yml ~
python3 path.py
cd
source ~/.bashrc
cd ~/Downloads/installCIF/GlobalServer
touch store.txt
touch IP_address.txt
yes | sudo apt install python3-flask
yes | sudo apt-get install python3-venv
python3 -m venv venv
. venv/bin/activate
pip install wheel
pip install Flask
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app &