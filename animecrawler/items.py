# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    aka = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    studio = scrapy.Field()
    rating = scrapy.Field(serializer=float)
    rating_count = scrapy.Field(serializer=int)
    tags = scrapy.Field()
    date = scrapy.Field()
