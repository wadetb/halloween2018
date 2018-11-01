#!/bin/sh
FLASK_ENV=development FLASK_APP=halloween.py python -m flask run --host=0.0.0.0 --port 5000
