#!/bin/bash
pip install --upgrade pip
pip install celery redis unicorn httpx neo4j networkx twisted scrapy requests googlesearch-python Flask beautifulsoup4 webdriver-manager yagooglesearch
pip install --upgrade Flask Werkzeug
export PYTHONPATH='${PYTHONPATH}:/home/user'
cd /home/user/backend
celery -A tasks worker --loglevel=info &
python /home/user/celery_app.py

