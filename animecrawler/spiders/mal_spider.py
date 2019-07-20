import urllib.error
from urllib.request import urlopen

import scrapy

from animecrawler.parser.mal_item_parser import MALItemParser
from animecrawler.utils.extract_utils import ExtractUtils


class MALSpider(scrapy.Spider):
    name = 'mal_1'
    anime_url = '{hostname}{path}'.format(hostname=ExtractUtils.MAL_URL, path='/anime.php?letter=')
    letters = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z']
    ANIMES_PER_PAGE = 50

    def start_requests(self):
        for letter in self.letters:
            print('version 1.0')
            yield scrapy.Request(url='{url}{letter}'.format(url=self.anime_url, letter=letter), callback=self.parse)

    def parse(self, response):
        urls = response.xpath(
            '//div[contains(@class, "js-categories-seasonal") or contains(@class, "list")]/table/tr[position()>1]/td[2]//a[contains(@class, "hovertitle") or contains(@class, "hoverinfo_trigger")]//@href').getall()

        for url in urls:
            yield scrapy.Request(url=url, callback=MALItemParser.parse_anime)

        letter_active = response.xpath(
            '//div[@id="horiznav_nav"]/ul/li/a[contains(@class, "horiznav_active")]//text()').get()
        if letter_active and letter_active == '#':
            letter_active = '.'

        url = response.request.url
        try:
            limit = int(url[url.index('show=') + 5:len(url)]) + self.ANIMES_PER_PAGE
        except ValueError:
            limit = self.ANIMES_PER_PAGE

        next_page = '{hostname}{path}{letter}&show={limit}'.format(hostname=ExtractUtils.MAL_URL,
                                                                   path='/anime.php?letter=', letter=letter_active,
                                                                   limit=limit)
        try:
            urlopen(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
        except urllib.error.HTTPError:
            print("done with the letter {} with {} limit".format(letter_active, limit - self.ANIMES_PER_PAGE))
