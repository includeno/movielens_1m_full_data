# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

class Movielens1MItemLoader(ItemLoader):
    pass

class Movielens1MItem(scrapy.Item):
    #['MovieID', 'name', 'url', 'time', 'genre', 'release_time', 'intro','Directors', 'Writers', 'Starts']
    id = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    name = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    time = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    genre = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    release_time = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    intro = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    directors = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    writers = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    starts = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
