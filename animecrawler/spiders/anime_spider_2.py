import scrapy
from animecrawler.parser.anime_item_parser import AnimeItemParser
from animecrawler.parser.anime_item_parser import ExtractUtils


class AnimesSpider2(scrapy.Spider):
    name = 'animes_2'
    anime_planet_url = 'https://www.anime-planet.com/anime/all'
    start_at = 0

    def start_requests(self):
        yield scrapy.Request(url=self.anime_planet_url, callback=self.get_urls)

    def get_urls(self, response):
        pages = (max(list(map(lambda str: int(str.replace("?page=", '')),
                              response.css('div.pagination.aligncenter li a::attr(href)').getall()))))
        urls = []
        self.start_at = pages // 5
        for i in range(self.start_at, (pages // 5) * 2):
            urls.append(self.anime_planet_url + '?page=' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.cardDeck.cardGrid a::attr(href)').extract():
            url = ExtractUtils.ANIME_PLANET_URL + href
            yield scrapy.Request(url, AnimeItemParser.parse_anime)
