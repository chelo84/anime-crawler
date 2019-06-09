import scrapy
from animecrawler.parser.anime_item_parser import AnimeItemParser
from animecrawler.utils.extract_utils import ExtractUtils


class AnimePlanetSpider(scrapy.Spider):
    name = 'anime_planet_4'
    all_anime_url = '{hostname}{path}'.format(hostname=ExtractUtils.ANIME_PLANET_URL, path='/anime/all')
    start_at = 0

    def start_requests(self):
        yield scrapy.Request(url=ExtractUtils.ANIME_PLANET_URL+'/anime/all', callback=self.get_urls)

    def get_urls(self, response):
        pages = (max(list(map(lambda str: int(str.replace("?page=", '')),
                              response.css('div.pagination.aligncenter li a::attr(href)').getall()))))
        urls = []
        self.start_at = (pages // 5) * 3
        for i in range(self.start_at, (pages // 5) * 4):
            urls.append(ExtractUtils.ANIME_PLANET_URL + '?page=' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('ul.cardDeck.cardGrid a::attr(href)').extract():
            url = ExtractUtils.ANIME_PLANET_URL + href
            yield scrapy.Request(url, AnimeItemParser.parse_anime)
