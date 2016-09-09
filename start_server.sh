#!/bin/bash

export FLASK_APP=server.py
FLASK_DEBUG=TRUE
flask run
echo 'Server started.'