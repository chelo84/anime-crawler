import scrapy
from animecrawler.parser.anime_item_parser import AnimeItemParser

class AnimesSpider4(scrapy.Spider):
    name = 'animes'
    anime_planet_url = 'https://www.anime-planet.com/anime/all'
    startAt = 0

    def start_requests(self):
        yield scrapy.Request(url=self.anime_planet_url, callback=self.get_urls)

    def get_urls(self, response):
        pages = (max(list(map(lambda str: int(str.replace("?page=", '')),
                              response.css('div.pagination.aligncenter li a::attr(href)').getall()))))
        urls = []
        self.startAt = (pages//5) * 3
        for i in range(self.startAt, (pages // 5) * 4):
            urls.append(self.anime_planet_url + '?page=' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.cardDeck.cardGrid a::attr(href)').extract():
            url = 'https://www.anime-planet.com' + href
            yield scrapy.Request(url, AnimeItemParser.parse_anime)
