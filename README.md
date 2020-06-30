# things_web

A web frontend, api and websocket connection for things attached through serial as arduinos or other microdevices would be

## installation

cd things_web/tools/setup

python3 -m venv ~/venvs/things_web

source ~/venvs/things_web/bin/activate

pip install -U pip

pip install -r requirements_dev.txt

## start

cd things_web/things_web

source ~/venvs/things_web/bin/activate

python things_web.py

## configuration

after first start in homefolder/things/things_web.json
