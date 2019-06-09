import scrapy
from animecrawler.parser.anime_item_parser import AnimeItemParser
from animecrawler.parser.anime_item_parser import ExtractUtils


class MALSpider(scrapy.Spider):
    name = 'mal_1'
    anime_url = '{hostname}{path}'.format(hostname=ExtractUtils.MAL_URL, path='/anime.php?letter=')
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F']
    rate = 1

    def __init__(self):
        # Sets the maximum pages downloaded per second
        self.download_delay = 1/float(self.rate)

    def start_requests(self):
        print(self.anime_url)
        for letter in self.letters:
            yield scrapy.Request(url='{url}{letter}'.format(url=self.anime_url, letter=letter), callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[contains(@class, "js-categories-seasonal") or contains(@class, "list")]/table/tr[position()>1]/td[2]//a[contains(@class, "hovertitle") or contains(@class, "hoverinfo_trigger")]//@href').getall()
        for url in urls:
            yield scrapy.Request(url, MALItemParser.parse_anime)
        # for href in response.css('ul.cardDeck.cardGrid a::attr(href)').extract():
        #     url = ExtractUtils.ANIME_PLANET_URL + href
        #     yield scrapy.Request(url, AnimeItemParser.parse_anime)
