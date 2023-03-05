import scrapy
from ..lib.ScrollSeleniumRequest import ScrollSeleniumRequest
from ..jscode import jump_to_bottom2
from ..items import Movielens1MItem,Movielens1MItemLoader

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

keywords=['Hommage à Zgougou ', 'Jon Stewart Has Left the Building ',
       'Bungou Stray Dogs']

class ImdbSearchSpider(scrapy.Spider):
    name = 'imdb_search'
    allowed_domains = ['imdb.com']
    start_urls = ['http://imdb.com/']
    base_url='http://imdb.com/'

    def start_requests(self):
        for keyword in keywords:
            yield ScrollSeleniumRequest(url=self.base_url,extra_info={"url":str(self.base_url),"keyword":keyword})

    def parse(self, response):
        pass
