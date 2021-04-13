#!/bin/bash
line="LPUSH HfutSpider:start_urls http://www.hfut.edu.cn/"
echo $line | redis-cli -h localhost -p 6379
sleep 10s
source activate searEngine
cd /home/xutianyuan/SearchProj/Search/SearchSpider
python main.py &
sleep 10s
cd /home/xutianyuan/SearchProj/Search/SearchSpiderChild
python main.py &
cd /home/xutianyuan/SearchProj/Search/SearchSpiderChild1
python main.py &
cd /home/xutianyuan/SearchProj/Search/ElasticSearchSave
python PictureTextFile.py &
