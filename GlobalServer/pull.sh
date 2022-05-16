#!/bin/bash -i
cd ~/Downloads/installCIF/GlobalServer
cif --tags honeypot --itype ipv4 --last-hour -f csv --columns indicator,lasttime | tail -n +2 | sed -e 's/"//g' > IP_address_time.txt
python3 update.py
python3 cleaner.py
python3 lineCounter.py