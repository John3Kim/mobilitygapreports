#!/bin/bash
# For unix only
VENV_PATH=virtualenv

if [ ! -f "$VENV_PATH" ]; then
    python3 -m venv virtualenv
    pip3 install -r requirements.txt
fi

source virtualenv/bin/activate