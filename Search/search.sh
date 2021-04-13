#!/bin/bash
source activate searEngine
cd /home/xutianyuan/SearchProj/Search/HfutSearch
python manage.py runserver 0.0.0.0:8001 &
