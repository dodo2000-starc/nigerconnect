#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python init_db.py
python seed_data.py