import scrapy
from ..lib.ScrollSeleniumRequest import ScrollSeleniumRequest
from ..jscode import jump_to_bottom2
from ..items import Movielens1MItem,Movielens1MItemLoader

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

import pymysql

def create_connection():
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='root123456',
                            database='spider',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_urls(count):
    connection=create_connection()
    cursor=connection.cursor()
    if(count==None):
        count=10
    # 查询语句
    sql = f"SELECT id, name, url FROM imdb_movies_links WHERE spider_completed=0 LIMIT {count}"

    # 执行查询
    cursor.execute(sql)
    results = cursor.fetchall()
    result_list=[]
    for result in results:
        result_list.append(result["url"])
    return result_list

class ImdbDetailSpider(scrapy.Spider):
    name = 'imdb_detail'
    allowed_domains = ['imdb.com']
    start_urls = [
        'https://www.imdb.com/title/tt0104257/?ref_=tt_tpks_tt_i_3_pd_tp1_pbr_ic',
        # 'https://www.imdb.com/title/tt1630029/?ref_=tt_rvi_tt_i_4',
        # 'https://www.imdb.com/title/tt0114168/?ref_=nv_sr_srsg_0',
        # 'https://www.imdb.com/title/tt0112346/?ref_=fn_al_tt_1',
        ]
    #start_urls=list(urls)

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
    
    def start_requests(self):
        #页面加载完毕立即执行
        script='window.scrollTo(0, document.body.scrollHeight);'
        
        #等待数量更新的元素
        wait_element=(By.CLASS_NAME, 'ipc-metadata-list__item')#sc-eda143c4-4 sc-b5e8e7ce-1
        wait_script=jump_to_bottom2(15,100)
        wait_count=10
        wait_until_list=[
            (By.CLASS_NAME, 'ipc-page-section'),
            (By.CLASS_NAME, 'ipc-metadata-list__item'),
            (By.CLASS_NAME,'ipc-html-content'),
            (By.CLASS_NAME,'ipc-inline-list__item'),
            (By.CLASS_NAME,'ipc-metadata-list-item__list-content-item'),
        ]

        self.start_urls=get_urls(2)
        # wait_time=10,
        # wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'ipc-metadata-list'))
        for url in self.start_urls:
            yield ScrollSeleniumRequest(url=url,wait_until=wait_element,wait_until_list=wait_until_list,wait_time=20, callback=self.parse, script=script, wait_element=wait_element,wait_count=wait_count,wait_script=wait_script,extra_info={"url":str(url)})

    def parse(self, response):
        temp = Movielens1MItemLoader(item=Movielens1MItem(), selector=response)
        request=response.request
        time.sleep(10)

        extra_info=request.meta["extra_info"]
        if(extra_info):
            temp.add_value("url",extra_info["url"])

        details_section = response.xpath('//section[@data-testid="Details"]')
        release_date = details_section.xpath('.//div[@data-testid="title-details-section"]/ul/li[@data-testid="title-details-releasedate"]//div/ul/li/a/text()'
                                             ).get()
        languages = details_section.xpath('.//div[@data-testid="title-details-section"]/ul/li[@data-testid="title-details-languages"]/div/ul/li')
        language_list=[]
        for language_selector in languages:
            language=language_selector.xpath('.//a/text()').get()
            print(language)
            language_list.append(language)
        # Details->Release date
        print("Release date:", release_date)
        temp.add_value("release_time",release_date)
        print("Languages:", language_list)

        # select section with class "sc-eda143c4-4 hbMdUH"
        elements = response.xpath('//section[@class="sc-eda143c4-4 hbMdUH"]/li[@class="ipc-metadata-list__item"]')
        print("elements:")
        print(elements)
        
        # extract information for each element
        for element in elements:
            label = element.xpath('.//button[@class="ipc-metadata-list-item__label"]/text()')
            value = element.xpath('.//li[@class="ipc-inline-list__item"]/a/text()')
            print("label:")
            print(label)
            print("value:")
            print(value)
            
            # format the output and yield it
            if label and value:
                
                value_str = ",".join([v.strip() for v in value.getall()])
                yield {label.strip(): value_str}
        
        title_section = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1[@data-testid="hero__pageTitle"]')
        print("title_section:"+str(title_section))
        name=title_section.xpath('.//span/text()').get()
        print("name:"+str(name))
        temp.add_value("name",str(name))
        temp.add_value("id",'1')

        # //*[@id="__next"]/main/div/section[contains(@class, 'newstime4')]
        # TechSpecs data-testid="TechSpecs"->title-techspec_runtime
        TechSpecSection = response.xpath('//section[@data-testid="TechSpecs"]/div')
        print("TechSpecSection:"+str(TechSpecSection.get()))
        time_str=TechSpecSection.xpath('.//li[@data-testid="title-techspec_runtime"]/div/text()').getall()
        print("time:"+str(''.join(time_str)))
        temp.add_value("time",str(''.join(time_str)))
        
        genres=response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[@class="ipc-chip-list__scroller"]/a')
        genres_str=[]
        for genre in genres:
            val=genre.xpath('.//span[@class="ipc-chip__text"]/text()').get()
            genres_str.append(str(val))
        print("genre:"+str('|'.join(genres_str)))
        temp.add_value("genre",str('|'.join(genres_str)))

        
        intro=response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[3]/text()').get()
        temp.add_value("intro",intro)
        temp.add_xpath("directors",'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li/a/text()')
        writers=response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul/li')
        writers_str=[]
        for writer in writers:
            val=writer.xpath('.//a/text()').get()
            writers_str.append(str(val))
        temp.add_value("writers",'|'.join(writers_str))
        starts=response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul/li')
        start_str=[]
        for start in starts:
            val=start.xpath('.//a/text()').get()
            start_str.append(str(val))
        print("start_str:")
        print(str('|'.join(start_str)))
        temp.add_value("starts",str('|'.join(start_str)))
        yield temp.load_item()
        
