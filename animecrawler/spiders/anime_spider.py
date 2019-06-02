import scrapy
# import re
# from animecrawler.utils.extract_utils import ExtractUtils
# from animecrawler.items import AnimeItem
from animecrawler.parser.anime_item_parser import AnimeItemParser

class AnimesSpider1(scrapy.Spider):
    name = 'animes'
    anime_planet_url = 'https://www.anime-planet.com/anime/all'
    start_at = 1

    def start_requests(self):
        yield scrapy.Request(url=self.anime_planet_url, callback=self.get_urls)

    def get_urls(self, response):
        pages = (max(list(map(lambda str: int(str.replace("?page=", '')),
                              response.css('div.pagination.aligncenter li a::attr(href)').getall()))))
        urls = []
        for i in range(self.start_at, pages // 5):
            urls.append(self.anime_planet_url + '?page=' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.cardDeck.cardGrid a::attr(href)').extract():
            url = 'https://www.anime-planet.com' + href
            yield scrapy.Request(url, AnimeItemParser.parse_anime)
