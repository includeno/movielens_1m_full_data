# 爬取IMDB网站补全 Movielens 1m数据

Python

scrapy+selenium+csv+mysql

# Generate requirements.txt
pip install pipreqs
pipreqs .

## scrapy

### 初始化

scrapy startproject movielens1m

###
cd movielens1m
scrapy genspider imdb_detail imdb.com
scrapy crawl imdb_detail

cd movielens1m
scrapy genspider imdb_search imdb.com