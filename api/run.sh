#!/bin/bash -e

# Replace PATH/TO/API with the actual path to your API directory (the one containing app.py and the venv)
. ~/PATH/TO/API/venv/bin/activate
cd ~/Flask/Minims
exec gunicorn -w 2 -b unix:PATH/TO/API/web.sock \
    --log-file - app:app