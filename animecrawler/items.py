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
    score = scrapy.Field(serializer=float)
    scored_by = scrapy.Field(serializer=int)
    tags = scrapy.Field()
    date = scrapy.Field()
    image = scrapy.Field()
    characters = scrapy.Field()

class MALItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    episodes = scrapy.Field()
    status = scrapy.Field()
    aired_from = scrapy.Field()
    aired_to = scrapy.Field()
    premiered = scrapy.Field()
    broadcast = scrapy.Field()
    producers = scrapy.Field()
    licensors = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    genres = scrapy.Field()
    duration = scrapy.Field()
    rating = scrapy.Field()
    score = scrapy.Field()
    scored_by = scrapy.Field()
    ranked = scrapy.Field()
    popularity = scrapy.Field()
    members = scrapy.Field()
    synopsis = scrapy.Field()
    characters = scrapy.Field()